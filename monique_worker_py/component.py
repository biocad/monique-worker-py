import zmq
import logging
import argparse
from monique_worker_py.config import read_component_config


class Component:
    def __init__(self, name):
        self.name = name

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', required=True, help='Path to config file')
        args = parser.parse_args()
        self.component_config = read_component_config(args.config)

    def initialize(self):
        """Initialize component and connect it to queue"""
        logging.basicConfig(level=self.component_config.log_level,
                            format='%(asctime)s %(name)-12s %(levelname)-8s {}: %(message)s'.format(self.name),
                            datefmt='%Y-%m-%d %H:%M',
                            filename=self.component_config.log_path,
                            filemode='a')

        logging.info("connecting to queue...")
        # setup connection
        context = zmq.Context()

        # Socket to receive messages from queue
        from_queue = context.socket(zmq.SUB)
        from_queue.connect(self.component_config.queue_sub_address())
        # listen only userdata messages
        from_queue.setsockopt(zmq.SUBSCRIBE, b"userdata")

        # Socket to send messages to queue
        to_queue = context.socket(zmq.PUSH)
        to_queue.connect(self.component_config.queue_push_address())

        logging.info("connected to queue.")
        return to_queue, from_queue
