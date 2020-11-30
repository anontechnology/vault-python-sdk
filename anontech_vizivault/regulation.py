from json_object import JSONObject


class Regulation(JSONObject):
    def __init__(self, name=None, key=None, url=None, rule=None):
        super().__init__()
        self.key = key
        self.name = name
        self.url = url
        self.rule = rule
        self.__created_date = None
        self.__modified_date = None

    @classmethod
    def from_json_dict(cls, json_dict):
        new_regulation = cls(
            key=json_dict['key'],
            name=json_dict['name'],
            url=json_dict['url'])
        new_regulation.__created_date = json_dict['createdDate']
        new_regulation.__modified_date = json_dict['modifiedDate']
        return new_regulation
