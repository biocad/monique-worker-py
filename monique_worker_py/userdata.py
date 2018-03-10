import json
import time


class Userdata(object):
    """
    This class describe Userdata, that one of the base messages in Monique system.
    JSON format is the following:
    {
        "user":"00000000-0000-0000-0000-000000000000",
        "property": String,
        "time": Int, ms,
        "type": String,
        "data": JSON
    }
    where
      * property - can be "created", "touched", "saved", "shared". Let it be "created" everytime;
      * type - identity name for data. For example, "biocad:production:strelna:line1:module2" or
        "biocad:moscow:laboratory:rna:temperature5";
      * data - content what we send via Userdata in JSON format.
    """
    def __init__(self, j):
        self.__dict__ = j

    def create_tag_and_tags(self):
        tags = [{'getTag': 'userdata'}]
        tag = 'U'
        return tag, tags

    def to_json(self):
        """Converts Userdata to JSON."""
        return json.dumps(self, allow_nan=False, default=lambda o: o.__dict__).encode("utf8")

    def get_type(self):
        """Returns 'type' field"""
        return self.type


def create_userdata(data_user, data_type, data_data, data_property="created"):
    now = current_millis()
    obj = {'user': data_user,
           'property': data_property,
           'time': now,
           'type': data_type,
           'data': data_data}
    return Userdata(obj)


def current_millis():
    """Get current time in milliseconds,"""
    return int(round(time.time() * 1000))
