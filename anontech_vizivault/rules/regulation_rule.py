from abc import ABC


class RegulationRule(ABC):

    def __init__(self, reg_type):
        self.type = reg_type
