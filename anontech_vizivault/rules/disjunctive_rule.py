from anontech_vizivault.rules.regulation_rule import RegulationRule


class DisjunctiveRule(RegulationRule):

    def __init__(self, type):
        self.constraints = []
        super().__init__("any")

    def add_rule(self, rule: RegulationRule):
        if not isinstance(rule, RegulationRule):
            raise TypeError(
                'Argument rule is not of type RegulationRule'
            )
        self.constraints.append(rule)
