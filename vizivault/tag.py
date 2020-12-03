from vizivault.json_object import JSONObject


class Tag(JSONObject):

    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.createdDate = None
        self.modifiedDate = None

    @classmethod
    def from_json_dict(cls, json_dict):
        new_tag = cls(json_dict['name'])
        new_tag.createdDate = json_dict['createdDate']
        new_tag.modifiedDate = json_dict['modifiedDate']
        return new_tag
