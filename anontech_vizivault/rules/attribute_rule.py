from enum import Enum
from anontech_vizivault.rules.regulation_rule import RegulationRule


class AttributeListOperator(Enum):
    ANY = 'any',
    NONE = 'none'


class AttributeRule(RegulationRule):

    def __init__(self, attributes=None, operator=None):
        self.attributes = attributes or []
        self.__operator = self.__get_operator(operator)
        super().__init__("attribute")

    @property
    def attribute_list_operator(self):
        return self.__operator.value

    @attribute_list_operator.setter
    def attribute_list_operator(self, operator: str):
        self.__operator = AttributeListOperator(operator)

    @staticmethod
    def __get_operator(operator):
        if isinstance(operator, AttributeListOperator):
            operator_obj = operator
        elif isinstance(operator, str):
            operator_obj = AttributeListOperator(operator)
        else:
            raise TypeError(
                'Argument operator is not of type AttributeListOperator'
            )
        return operator_obj
