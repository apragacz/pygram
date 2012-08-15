class SymbolLocation(object):
    def __init__(self, filename=None, start_line=None, start_column=None,
                    end_line=None, end_column=None):
        self._filename=filename
        self._start_line = start_line
        self._start_column = start_column

class Symbol(object):
    pass

class TerminalSymbol(object):
    def __init__(self, t, value, filename=None, line=None, column=None):
        self._type = t
        self._value = value
        self._filename=filename
        self._line = line
        self._column = column
