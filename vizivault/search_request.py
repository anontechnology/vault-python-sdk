from json_object import JSONObject


class SearchRequest(JSONObject):

    def __init__(self, attribute=None, value=None):
        super().__init__()
        self.regulations = []
        self.values = []
        self.attributes = []

        if attribute is not None and value is not None:
            self.add_value_query(attribute, value)

        self.sensitivity = None
        self.userId = None
        self.country = None
        self.subdivision = None
        self.city = None
        self.minCreatedDate = None
        self.maxCreatedDate = None
        self.minModifiedDate = None
        self.maxModifiedDate = None

    def add_value_query(self, attribute, value):
        self.values.append(self.ValueSearchRequest(attribute, value))

    class ValueSearchRequest:
        def __init__(self, attribute, value):
            self.attribute = attribute
            self.value = value

    @classmethod
    def from_json_dict(cls, json_dict):
        new_search = cls(
            attribute=None,
            value=None
        )
        new_search.regulations = json_dict['regulations']
        new_search.values = json_dict['values']
        new_search.attributes = json_dict['attributes']
        new_search.sensitivity = json_dict['sensitivity']
        new_search.userId = json_dict['userId']
        new_search.city = json_dict['city']
        new_search.minCreatedDate = json_dict['minCreatedDate']
        new_search.maxCreatedDate = json_dict['maxCreatedDate']
        new_search.minModifiedDate = json_dict['minModifiedDate']
        new_search.maxModifiedDate = json_dict['maxModifiedDate']
