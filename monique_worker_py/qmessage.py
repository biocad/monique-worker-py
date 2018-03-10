import json
from monique_worker_py.task import Task, create_task
from monique_worker_py.userdata import Userdata


class QMessage(object):
    """
    QMessage is wrapper for messages in Monique.
    It will be refactored later.
    But now JSON structure is the following:
    {
      "tags":
        [
        -- in Task case:
        [
          {"getTag": String},  # fixed field, equal "task"
          {"getTag": String},  # status field, equal to field "status" in Task
          {"getTag": String}   # spec field, equal to field "spec" in Task
        ],
        -- in Userdata case:
        [
          {"getTag": String}   # fixed field, equal "userdata"
        ],
      "cnt":{
        "tag": String,         # fixed field, equal "T" in Task case and "U" in Userdata case
        "contents": JSON       # field that contains Task or Userdata in JSON format
      },

    JSON Task example:
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

    JSON Userdata example:
    {
      "tags":[
        {"getTag":"userdata"}
      ],
      "cnt":{
        "tag":"U",
        "contents":{
          "user":"00000000-0000-0000-0000-000000000000",
          "property":"created",
          "time":1520701240542,
          "type":"biocad:production:strelna:line1:module1",
          "data":1
        }
      }
    }
    """
    def __init__(self, j):
        self.__dict__ = j
        self.tags = j['tags']
        self.cnt = Contents(j['cnt'])

    def get_content(self):
        """Returns field "contents" from QMessage"""
        return self.cnt.contents

    def to_json(self):
        """Convert QMessage to JSON."""
        return json.dumps(self, allow_nan=False, default=lambda o: o.__dict__).encode("utf8")


class Contents:
    """
        Contents describe "cnt" field in qmessage task
    """
    def __init__(self, json_dict):
        self.tag = json_dict['tag']
        if self.tag == 'T':
            self.contents = Task(json_dict['contents'])
        elif self.tag == 'U':
            self.contents = Userdata(json_dict['contents'])
        else:
            raise Exception("Unknown tag")


def qmessage_from_json(data):
    """Converts QMessage from JSON format."""
    in_json = json.loads(data.decode('utf8').replace("'", '"'))
    return QMessage(in_json)


def create_qmessage(some_data):
    """Creates qmessage from some data. At current moment data can be Task or Userdata"""
    tag, tags = some_data.create_tag_and_tags()
    obj = {'tags': tags, 'cnt': {'tag': tag, 'contents': some_data.__dict__}}
    return QMessage(obj)