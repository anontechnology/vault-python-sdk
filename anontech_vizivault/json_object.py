from abc import ABC, abstractmethod
import json
import datetime
from enum import Enum
from json import JSONEncoder
import re


class JSONObject(ABC):
    def __init__(self):
        self.default_encoder = self.MyJSONEncoder

    def to_json(self, encoder_class=None):
        encoder_class = encoder_class or self.default_encoder
        return json.dumps(self, cls=encoder_class,
                          sort_keys=True, indent=4)

    class MyJSONEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat
            elif isinstance(obj, Enum):
                return obj.value[0]
            else:
                d = {}
                for key, value in obj.__dict__.items():
                    if value is None:
                        continue
                    elif key == "default_encoder":
                        continue
                    else:
                        d[re.sub(r'^_{1,2}\w+_{2,}', '', key)] = value
                return d

    @classmethod
    def from_json(cls, json_bytes):
        json_obj = json.loads(json_bytes)['data']
        if isinstance(json_obj, list):
            return [cls.from_json_dict(json_dict) for json_dict in json_obj]
        else:
            return cls.from_json_dict(json_obj)

    @classmethod
    @abstractmethod
    def from_json_dict(cls, json_dict: dict):
        # Should add some kind of validation object is serialized class here
        pass
