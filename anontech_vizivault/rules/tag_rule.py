from enum import Enum
from anontech_vizivault.rules.regulation_rule import RegulationRule


class TagListOperator(Enum):
    ANY = "any",
    NONE = "none",
    ALL = "all"


class TagRule(RegulationRule):

    def __init__(self, attributes=None, operator=None):
        self.__operator = self.__get_operator(operator)
        self.__attributes = attributes or []
        super().__init__("attribute")

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, operator: str):
        self.__operator = self.__get_operator(operator)

    @staticmethod
    def __get_operator(operator):
        if isinstance(operator, TagListOperator):
            my_operator = operator
        elif isinstance(operator, str):
            my_operator = TagListOperator(operator)
        else:
            raise TypeError('Argument operator is not of type TagListOperator')
        return my_operator
