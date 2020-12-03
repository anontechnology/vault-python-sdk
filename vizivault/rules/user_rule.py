from enum import Enum
from vizivault.rules.regulation_rule import RegulationRule


class UserValuePredicate(Enum):
    EQUALS = 'eq',
    NOT_EQUALS = 'neq',
    LESS_THAN = 'lt',
    GREATER_THAN = 'gt',
    LESS_OR_EQUAL = 'leq',
    GREATER_OR_EQUAL = 'geq',
    BEFORE = 'before',
    AFTER = 'after'


class UserRule(RegulationRule):

    def __init__(self, attribute=None, predicate=None, value=None):
        self.attribute = attribute
        self.value = value
        self.__predicate = self.__get_predicate(predicate)

        super().__init__("user")

    @property
    def predicate(self):
        return self.__predicate

    @predicate.setter
    def predicate(self, user_value_predicate: str):
        self.__predicate = UserValuePredicate(user_value_predicate)

    @staticmethod
    def __get_predicate(predicate):
        if isinstance(predicate, UserValuePredicate):
            predicate_obj = predicate
        elif isinstance(predicate, str):
            predicate_obj = UserValuePredicate(predicate)
        else:
            raise TypeError(
                'Argument predicate is not of type UserValuePredicate'
            )
        return predicate_obj
