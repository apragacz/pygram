class SymbolLocation(object):
    def __init__(self, filename=None, start_line=None, start_column=None,
                    end_line=None, end_column=None):
        self._filename = filename
        self._start_line = start_line
        self._start_column = start_column
        self._end_line = end_line


class Symbol(object):
    def __init__(self, t, value, location=None):
        self._type = t
        self._value = value
        self._location = location

    @property
    def type(self):
        return self._type


class GrammarRule(object):
    def __init__(self, input_type, output_types, composite_function=None):
        self._input_type = input_type
        self._output_types = output_types
        self._composite_fun = composite_function


class ReductionRule(object):
    #TODO
    pass
