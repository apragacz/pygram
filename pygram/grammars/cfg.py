from .base import GrammarRule, Grammar


class ContextFreeGrammarRule(GrammarRule):
    def __init__(self, head_symbol, body_symbols):
        self._head_symbol = head_symbol
        self._body_symbols = tuple(body_symbols)

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


class ContextFreeGrammar(Grammar):
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
