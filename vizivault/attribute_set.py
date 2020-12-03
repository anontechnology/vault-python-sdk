from vizivault.attribute import Attribute
from vizivault.json_object import JSONObject


class AttributeSet(JSONObject):
    def __init__(self, attributes):
        super().__init__()
        self.data = attributes or []

    def add_attribute(self, attribute):
        if not isinstance(attribute, Attribute):
            raise TypeError(
                'Argument attribute is not of type Attribute'
            )
        self.data.append(attribute)

    @classmethod
    def from_json_dict(cls, json_dict):
        return cls(
            attributes=json_dict['data'])
