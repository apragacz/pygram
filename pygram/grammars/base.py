from .symbols import SymbolInstance


class ContextFreeGrammarRule(object):
    def __init__(self, head_symbol, body_symbols):
        self._head_symbol = head_symbol
        self._body_symbols = body_symbols

    @property
    def rule(self):
        return self

    @property
    def head_symbol(self):
        return self._head_symbol

    @property
    def body_symbols(self):
        return self._body_symbols

    def __unicode__(self):
        return u'%s -> %s' % (unicode(self._head_symbol),
                                u' '.join([unicode(bs)
                                            for bs in self._body_symbols]))


class Reduction(object):
    def __init__(self, rule, callback=None):
        self._rule = rule
        self._callback = callback

    @property
    def rule(self):
        return self._rule

    def reduce_instances(self, symbol_instances):
        assert(len(symbol_instances) == len(self._rule.body_symbol_types))
        assert(all([si.symbol == bs for si, bs in (symbol_instances,
                                                self._rule.body_symbols)]))
        value = self._callback(*[si.value for si in symbol_instances])
        return SymbolInstance(symbol=self._rule.head_symbol, value=value)

    def __unicode__(self):
        r'%s with reduction callback %s' (unicode(self._rule, self._callback))


class ContextFreeGrammar(object):
    def __init__(self, nonterm_symbols, term_symbols, rules,
                start_symbol):
        self._nonterm_symbols = nonterm_symbols
        self._term_symbols = term_symbols
        self._rules = rules
        self._start_symbol = start_symbol


class ContextFreeGrammarProcessor(object):
    def __init__(self, nonterm_symbols, term_symbols, reductions,
                start_symbol):
        self._nonterm_symbols = nonterm_symbols
        self._term_symbols = term_symbols
        self._reductions = reductions
        self._start_symbol = start_symbol
