import json
import time


class Task(object):
    """
    This class describe Task, that one of the base messages in Monique system.
    JSON format is the following:
    {
        "id": String,
        "pid": null or String,
        "spec": String,
        "user":"00000000-0000-0000-0000-000000000000",
        "status": String,
        "creation_time": Int, ms,
        "modification_time": Int, ms,
        "config": JSON,
        "result": null or {"content": JSON,
                           "version": Int},
        "message": null or String
    }
    """
    def __init__(self, j):
        self.__dict__ = j

    def task_completed(self, worker_result):
        """Makes task completed. We should update time, status and result fields."""
        self.status = 'completed'
        self.modification_time = current_millis()
        self.result = {'content': worker_result.result,
                       'version': worker_result.version}
        return self

    def task_failed(self, worker_name, error):
        """Make task failed. We should update time, status and message fields."""
        self.status = 'failed'
        self.modification_time = current_millis()
        self.message = '{} (worker): {}'.format(worker_name, error)
        return self

    def to_json(self):
        """Converts Task to JSON."""
        return json.dumps(self, allow_nan=False, default=lambda o: o.__dict__).encode("utf8")

    def get_config(self):
        """Returns config from Task."""
        return self.config


def create_task(task_id, task_user, task_spec, task_config, task_pid=None):
    now = current_millis()
    obj = {'id': task_id,
           'pid': task_pid,
           'spec': task_spec,
           'user': task_user,
           'status': 'new',
           'creation_time': now,
           'modification_time': now,
           'config': task_config,
           'result': None,
           'message': None}
    return Task(obj)


def create_task_id():
    """
    Creates new task ID. It is probably not too safe, but now it is current time with big precision.
    It will be refactored later.
    """
    return str(int(round(time.time() * 10**9)))


def current_millis():
    """Get current time in milliseconds,"""
    return int(round(time.time() * 1000))