class Statement(object):
    pass


class CompoundStatement(object):

    def __init__(self, suite):
        self._suite = suite


class FunctionStatement(CompoundStatement):
    pass
