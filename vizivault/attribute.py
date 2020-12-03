from json_object import JSONObject


class Attribute(JSONObject):

    def __init__(self, data_point_id=None, userId=None, attribute=None, sensitivity=None, value=None, regulations=None,
                 tags=None, created_date=None, modified_date=None):
        super().__init__()
        self.dataPointId = data_point_id
        self.userId = userId
        self.attribute = attribute
        self.sensitivity = sensitivity
        self.value = value
        self.regulations = regulations or []
        self.tags = tags or []
        self.createdDate = created_date
        self.modifiedDate = modified_date

    @classmethod
    def from_json_dict(cls, json_dict: dict):
        return cls(
            data_point_id=json_dict['dataPointId'],
            userId=json_dict['userId'],
            attribute=json_dict['attribute'],
            sensitivity=json_dict['sensitivity'],
            value=json_dict['value'],
            regulations=json_dict['regulations'],
            tags=json_dict['tags'],
            created_date=json_dict['createdDate'],
            modified_date=json_dict['modifiedDate'])
