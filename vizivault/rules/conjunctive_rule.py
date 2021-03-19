from vizivault.rules.regulation_rule import RegulationRule


class ConjunctiveRule(RegulationRule):

    def __init__(self):
        self.constraints = []
        super().__init__("all")

    def add_rule(self, rule: RegulationRule):
        if not isinstance(rule, RegulationRule):
            raise TypeError(
                'Argument rule is not of type RegulationRule'
            )
        self.constraints.append(rule)
