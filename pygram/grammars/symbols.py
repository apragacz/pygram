from collections import Set


class Symbol(object):
    def __init__(self, name, symbol_set):
        self._symbol_set = symbol_set
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._name != other._name:
            return False
        if self._symbol_set != other._symbol_set:
            return False
        return True

    def __unicode__(self):
        return unicode(self._name)


class SymbolSet(Set):
    def __init__(self, name):
        self._name = name
        self._symbols = []

    def new_symbol(self, name=None):
        if name is None:
            name = '%s%d' % (self._name, len(self._symbols))
        symbol = Symbol(name, self)
        self._symbols.append(symbol)
        return symbol

    def __list__(self):
        return list(self._symbols)

    def __tuple__(self):
        return tuple(self._symbols)

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, key):
        return self._symbols[key]

    def __len__(self, key):
        return len(self._symbols)

    def __unicode__(self):
        return u'{%s}' % [unicode(s) for s in self._symbols]


class FileLocation(object):
    def __init__(self, filename=None, start_line=None, start_column=None,
                    end_line=None, end_column=None):
        self._filename = filename
        self._start_line = start_line
        self._start_column = start_column
        self._end_line = end_line


class SymbolInstance(object):
    def __init__(self, symbol, value, location=None):
        self._symbol = symbol
        self._value = value
        self._location = location

    @property
    def symbol(self):
        return self._symbol

    @property
    def value(self):
        return self._value
