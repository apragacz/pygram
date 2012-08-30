class Token(object):
    def __init__(self, symbol, value=None, location=None):
        self._symbol = symbol
        self._value = value
        self._location = location

    @property
    def symbol(self):
        return self._symbol

    @property
    def value(self):
        return self._value

    @property
    def location(self):
        return self._location
