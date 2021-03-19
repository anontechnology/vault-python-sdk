from vizivault.schema.primitive_schema import PrimitiveSchema
from json_object import JSONObject


class AttributeDefinition(JSONObject):

    def __init__(self, name, hint=None, repeatable=None, indexed=None, tags=None, schema=None):
        super().__init__()
        self.__key = name
        self.__name = name
        self.hint = hint

        self.repeatable = repeatable
        self.indexed = indexed
        self.__created_date = None
        self.__modified_date = None
        self.tags = tags or []
        self.schema = schema or PrimitiveSchema.STRING

    @classmethod
    def from_json_dict(cls, json_dict: dict):
        new_attribute_definition = cls(
            name=json_dict['name'],
            hint=json_dict['hint'],
            repeatable=json_dict['repeatable'],
            indexed=json_dict['indexed'],
            tags=json_dict['tags'],
            schema=json_dict['schema'],
        )
        new_attribute_definition.__created_date = json_dict['createdDate']
        new_attribute_definition.__modified_date = json_dict['modifiedDate']
        return new_attribute_definition

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name
        self.__key = name

    def schema_from_json(self, json_schema):
        self.schema = json_schema

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for key in self.__dict__:
                if key != 'methods':
                    if self.__dict__[key] != other.__dict__[key]:
                        return False
            return True
        return NotImplemented
