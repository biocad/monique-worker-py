import json
import time


class QMessage:
    def __init__(self, tags, cnt):
        self.tags = tags
        self.cnt = cnt

    def contents(self):
        return self.cnt['contents']

    def get_config(self):
        return self.contents()['config']

    def to_json(self):
        return json.dumps(self, allow_nan=False, default=lambda o: o.__dict__).encode("utf8")

    def task_completed(self, worker_result):
        self.contents()['status'] = 'completed'
        self.contents()['modification_time'] = current_millis()
        self.contents()['result'] = {'content': worker_result.result,
                                     'version': worker_result.version}
        self.tags[1]['getTag'] = 'completed'
        return self

    def task_failed(self, worker_name, error):
        self.contents()['status'] = 'failed'
        self.contents()['modification_time'] = current_millis()
        self.contents()['message'] = '{} (worker): {}'.format(worker_name, error)
        self.tags[1]['getTag'] = 'failed'
        return self


def qmessage_from_json(data):
    in_json = json.loads(data.decode('utf8').replace("'", '"'))
    return QMessage(in_json['tags'], in_json['cnt'])


def current_millis():
    return int(round(time.time() * 1000))