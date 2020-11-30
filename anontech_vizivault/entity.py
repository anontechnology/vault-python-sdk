from anontech_vizivault.attribute import Attribute
from itertools import chain
from json_object import JSONObject


class Entity(JSONObject):

    def __init__(self, entity_id, data=None):
        super().__init__()
        self.id = entity_id
        self.tags = []

        # All not repeated attributes
        self.__attributes = {}

        # Hash of List of Attributes that are repeated.
        self.__repeated_attributes = {}
        self.__changed_attributes = set()
        self.__deleted_attributes = set()

        if data is not None:
            for attribute in data:
                attribute_to_add = Attribute(data_point_id=attribute['dataPointId'],
                                             userId=attribute['userId'],
                                             attribute=attribute['attribute'],
                                             sensitivity=attribute['sensitivity'],
                                             value=attribute['value'],
                                             regulations=attribute['regulations'],
                                             tags=attribute['tags'],
                                             created_date=attribute['createdDate'],
                                             modified_date=attribute['modifiedDate'])
                self.add_attribute_without_pending_change(attribute_to_add)

    @property
    def changed_attributes(self):
        return list(self.__changed_attributes)

    @property
    def deleted_attributes(self):
        return list(self.__deleted_attributes)

    def add_attribute(self, attribute=None, value=None):
        if value is not None:
            attribute = Attribute(attribute=attribute, value=value)

        if isinstance(attribute, Attribute):
            self.add_attribute_without_pending_change(attribute)
            self.__changed_attributes.add(attribute)
        else:
            raise TypeError(
                'Argument attribute is not of type attribute or a string/value pair'
                ' that can be coerced into an attribute')

    def add_attribute_without_pending_change(self, attribute):
        attribute_key = attribute.attribute

        if attribute_key in self.__repeated_attributes:
            self.__repeated_attributes[attribute_key].append(attribute)
        # We have this attribute already so now it's a repeated attribute
        elif attribute_key in self.__attributes:
            # Remove the existing attribute and add BOTH to the repeated attributes dict
            self.__repeated_attributes[attribute_key] = [self.__attributes[attribute_key], attribute]
            del (self.__attributes[attribute_key])
        else:
            self.__attributes[attribute_key] = attribute

    def get_attribute(self, attribute_key):
        # We have to search repeated attribute and the attribute lists to determine what to return
        if attribute_key in self.__repeated_attributes:
            if len(self.__repeated_attributes[attribute_key]) == 1:
                attribute = self.__repeated_attributes[attribute_key][0]
            else:
                attribute = self.__repeated_attributes[attribute_key]
        elif attribute_key in self.__attributes:
            attribute = self.__attributes[attribute_key]
        else:
            attribute = None
        return attribute

    def get_attributes(self):
        return list(self.__attributes.values()) + list(chain.from_iterable(self.__repeated_attributes.values()))

    def purge(self):
        self.__attributes.clear()

    def clear_attribute(self, attribute_key):
        del (self.__attributes[attribute_key])
        del (self.__repeated_attributes[attribute_key])
        self.__deleted_attributes.add(attribute_key)

    @classmethod
    def from_json_dict(cls, json_dict):
        return cls(
            entity_id=json_dict['userId'],
            data=json_dict['data'])
