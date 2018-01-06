import json


class WorkerConfig:
    def __init__(self,
                 controller_host,
                 from_controller_port,
                 queue_host,
                 from_queue_port,
                 log_path,
                 log_level):  # see description here https://docs.python.org/3/library/logging.html#logging-levels
        self.controller_host = controller_host
        self.from_controller_port = from_controller_port
        self.queue_host = queue_host
        self.from_queue_port = from_queue_port
        self.log_path = log_path
        self.log_level = log_level

    def controller_pull_address(self):
        return "tcp://{}:{}".format(self.controller_host, self.from_controller_port)

    def controller_push_address(self):
        return "tcp://{}:{}".format(self.controller_host, self.from_controller_port + 1)

    def queue_sub_address(self):
        return "tcp://{}:{}".format(self.queue_host, self.from_queue_port)

    def queue_push_address(self):
        return "tcp://{}:{}".format(self.queue_host, self.from_queue_port + 1)


def read_config(path_to_config):
    data = json.load(open(path_to_config))
    deploy = data['deploy']['monique']
    controller_host = deploy['controller_host']
    controller_port = deploy['controller_port']
    queue_host = deploy['queue_host']
    queue_port = deploy['queue_port']
    log_path = deploy['log_path']
    log_level = deploy['log_level']
    return WorkerConfig(controller_host,
                        controller_port,
                        queue_host,
                        queue_port,
                        log_path,
                        log_level)
