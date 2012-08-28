from collections import Set, OrderedDict


class Symbol(object):
    def __init__(self, codename, display_name, symbol_set):
        self._symbol_set = symbol_set
        self._codename = codename
        self._display_name = display_name

    @property
    def codename(self):
        return self._codename

    @property
    def display_name(self):
        return self._display_name

    def __hash__(self):
        return hash(self._codename)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._codename != other._codename:
            return False
        if self._symbol_set != other._symbol_set:
            return False
        return True

    def __str__(self):
        return str(self._display_name)

    def __repr__(self):
        return '%s.%s' % (self._symbol_set.codename, self._codename)

    def __unicode__(self):
        return unicode(self._display_name)


class SymbolSet(Set):
    def __init__(self, codename, symbols_spec):
        self._codename = codename
        self._symbols = OrderedDict()
        for spec in symbols_spec:
            try:
                if not isinstance(spec, basestring):
                    sp = list(spec)
                else:
                    sp = [spec]
            except TypeError:
                sp = [spec]
            try:
                codename = sp[0]
                display_name = codename
            except IndexError:
                raise ValueError('symbol spec is empty')

            try:
                display_name = sp[1]
            except IndexError:
                pass

            if codename is None:
                codename = '%s%d' % (self._codename, len(self._symbols))
            if display_name is None:
                display_name = codename
            symbol = Symbol(codename, display_name, self)

            if codename in self._symbols:
                raise ValueError('symbol %s already exists' % codename)

            self._symbols[codename] = symbol

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._codename != other._codename:
            return False
        #test same symbol codenames, in the same order
        if self._symbols.keys() != other._symbols.keys():
            return False
        return True

    def __hash__(self):
        return hash(self._codename)

    def __iter__(self):
        return self._symbols.itervalues()

    def __getattr__(self, name):
        if name in self._symbols:
            return self._symbols[name]
        else:
            raise AttributeError('symbol %s is not defined' % name)

    def __getitem__(self, key):
        if key in self._symbols:
            return self._symbols[key]
        else:
            for s in self._symbols.itervalues():
                if s.display_name == key:
                    return s
            raise KeyError('symbol %s is not defined' % key)

    def __len__(self):
        return len(self._symbols)

    def __contains__(self, elem):
        return elem in self._symbols.values()

    def show(self, fun):
        return '%s([%s])' % (
                        self.__class__.__name__,
                        ', '.join([fun(s)
                                    for s in self._symbols.values()]))

    def __repr__(self):
        return '%s(%s, [%s])' % (
                        self.__class__.__name__,
                        self._codename,
                        ', '.join([s.codename for s in self._symbols.values()]))

    def __str__(self):
        return self.show(str)

    def __unicode__(self):
        return self.show(unicode)

    @property
    def codename(self):
        return self._codename


fundamental = SymbolSet('fundamental', [('empty', 'e'), ('end', '$')])
