from .base import GrammarRule, Grammar


class CFGRule(GrammarRule):
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

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._head_symbol != other._head_symbol:
            return False
        if self._body_symbols != other._body_symbols:
            return False
        return True

    def __hash__(self):
        return hash(self._head_symbol) + hash(self._body_symbols)

    def __unicode__(self):
        return u'%s -> %s' % (unicode(self._head_symbol),
                                u' '.join([unicode(bs)
                                            for bs in self._body_symbols]))


class CFG(Grammar):
    """ context-free grammar """
    def __init__(self, nonterm_symbols, term_symbols, rules,
                start_symbol):
        self._nonterm_symbols = nonterm_symbols
        self._term_symbols = term_symbols
        self._rules = tuple(rules)
        self._start_symbol = start_symbol

    def first_terminals(self, nonterm_symbol):
        pass

    def follow_terminals(self, nonterm_symbol):
        pass


class CFGExtended(CFG):
    """ context-free grammar enriched with reductions """
    def __init__(self, nonterm_symbols, term_symbols, reductions,
                start_symbol):
        rules = tuple((reduction.rule for reduction in reductions))
        super(CFGExtended, self).__init__(nonterm_symbols, term_symbols,
                                            rules, start_symbol)
        self._reductions = tuple(reductions)
