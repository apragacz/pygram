class Statement(object):
    pass


class CompoundStatement(Statement):
    pass


class IfElseStatement(CompoundStatement):
    def __init__(self, conditions_suites, else_suite):
        self._conditions_suites = conditions_suites
        self._else_suite = else_suite

    def interpret(self, context):
        pass
