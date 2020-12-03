from vizivault.entity import Entity


class User(Entity):

    def __init__(self, entity_id, data=None):
        super().__init__(entity_id=entity_id, data=data)

    def from_json_dict(cls, json_dict):
        super()
