import json
from monique_worker_py.task import Task, create_task


class QMessage(object):
    """
    QMessage is wrapper for messages in Monique.
    It will be refactored later.
    But now JSON structure is the following:
    {
      "tags":[
        {"getTag": String},    # fixed field, equal "task"
        {"getTag": String},    # status field, equal to field "status" in Task
        {"getTag": String}],   # spec field, equal to field "spec" in Task
      "cnt":{
        "tag": String,         # fixed field, equal "T"
        "contents": JSON       # Task field, contains Task in JSON format
      },

    JSON example:
    {
      "tags":[
        {"getTag":"task"},
        {"getTag":"new"},
        {"getTag":"exampleA"}
      ],
      "cnt":{
        "tag":"T",
        "contents":{
          "id":"1510727396541336165",
          "pid":null,
          "spec":"exampleA",
          "user":"00000000-0000-0000-0000-000000000000",
          "status":"new",
          "creation_time":1516950199392,
          "modification_time":1516950199392,
          "config":{
            "configA":"ASAASDASD"
          },
          "result":null,
          "message":null
        }
      }
    }
    """
    def __init__(self, j): # task <status task> <task name>
        self.__dict__ = j
        self.tags = j['tags']
        self.cnt = Contents(j['cnt']['tag'], Task(j['cnt']['contents']))

    def get_config(self):
        """Return config from task."""
        return self.cnt.contents.get_config()

    def to_json(self):
        """Convert QMessage to JSON."""
        return json.dumps(self, allow_nan=False, default=lambda o: o.__dict__).encode("utf8")

    def qmessage_completed(self, worker_result):
        """Return QMessage with completed Task inside. We also should update status for the second Tag."""
        self.cnt = Contents(self.cnt.tag, self.cnt.contents.task_completed(worker_result))
        self.tags[1]['getTag'] = 'completed'
        return self

    def qmessage_failed(self, worker_name, error):
        """Return QMessage with failed Task inside. We also should update status for the second Tag."""
        self.cnt = Contents(self.cnt.tag, self.cnt.contents.task_failed(worker_name, error))
        self.tags[1]['getTag'] = 'failed'
        return self


class Contents:
    def __init__(self, tag, contents):
        self.tag = tag
        self.contents = contents


def qmessage_from_json(data):
    """Converts QMessage from JSON format."""
    in_json = json.loads(data.decode('utf8').replace("'", '"'))
    return QMessage(in_json)


def create_qmessage(task_id, task_user, task_spec, task_config, task_pid=None):
    task = create_task(task_id, task_user, task_spec, task_config, task_pid)
    tags = [{'getTag': 'task'}, {'getTag': 'new'}, {'getTag': task_spec}]
    obj = {'tags': tags, 'cnt': {'tag': 'T', 'contents': task.__dict__}}
    return QMessage(obj)
