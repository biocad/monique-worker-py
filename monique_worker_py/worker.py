import zmq
import logging
import argparse
from monique_worker_py.config import read_config
from monique_worker_py.qmessage import qmessage_from_json


class Worker:
    def __init__(self, worker_name, algo):
        self.worker_name = worker_name
        self.algo = algo

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', required=True, help='Path to config file')
        args = parser.parse_args()
        self.worker_config = read_config(args.config)

    def run(self):
        """Runs application"""
        logging.basicConfig(level=self.worker_config.log_level,
                            format='%(asctime)s %(name)-12s %(levelname)-8s {}: %(message)s'.format(self.worker_name),
                            datefmt='%Y-%m-%d %H:%M',
                            filename=self.worker_config.log_path,
                            filemode='a')

        logging.info("connecting to queue...")
        # setup connection
        context = zmq.Context()

        # Socket to receive messages from controller
        from_controller = context.socket(zmq.PULL)
        from_controller.connect(self.worker_config.controller_pull_address())

        # Socket to send messages to controller
        to_controller = context.socket(zmq.PUSH)
        to_controller.connect(self.worker_config.controller_push_address())

        logging.info("connected to queue.")

        # waiting for the message...
        while True:
            in_message = from_controller.recv()
            logging.info('message received.')

            # parsing message to QMessage
            qmessage = qmessage_from_json(in_message)
            logging.debug('message tags: {}; message cnt: {}'.format(qmessage.tags, qmessage.cnt))

            # get config from Task
            config = qmessage.get_config()
            logging.info('config parsed')
            logging.debug('config content: {}'.format(config))

            try:
                logging.info('start working...')

                # that is the MAIN PLACE. We run given algorithm with config received.
                wr = self.algo(config)

                logging.debug('worker result: {}, worker version: {}'.format(wr.result, wr.version))
                logging.info('finished working!')

                # prepare result QMessage...
                completed_message = qmessage.qmessage_completed(wr)

                # and sending it back to the queue.
                logging.info('sending message with completed task...')
                logging.debug('message: {}'.format(completed_message.to_json()))
                to_controller.send(completed_message.to_json())

                logging.info("message sent :)")

            except Exception as e:
                logging.error('failed with error: {}'.format(e))

                # if exception happened then format result QMessage with another method...
                failed_message = qmessage.qmessage_failed(self.worker_name, e)

                # and sending it back.
                logging.info("sending message with failed task...")
                logging.debug('message: {}'.format(failed_message.to_json()))
                to_controller.send(failed_message.to_json())

                logging.info("message sent :(")


class WorkerResult:
    """Class to format worker result."""
    def __init__(self, result, version):
        self.result = result
        self.version = version
