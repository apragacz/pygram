from .base import GrammarRule, Grammar
from .symbols import fundamental


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
        self._first_terminals = {}
        self._follow_terminals = {}
        self._calculate_first_terminals()
        self._calculate_follow_terminals()

    def _calculate_first_terminals(self):
        self._first_terminals = {}
        for s in self._term_symbols:
            self._first_terminals[s] = set([s])

        for s in self._nonterm_symbols:
            self._first_terminals[s] = set([])
            if CFGRule(s, [fundamental.empty]) in self.rules_for_symbol(s):
                self._first_terminals[s].add(fundamental.empty)

        updated = True
        while updated:
            updated = False
            for s in self._nonterm_symbols:
                symbol_rules = self.rules_for_symbol(s)
                for r in symbol_rules:
                    for bs in r.body_symbols:

                        bs_first = self._first_terminals[bs]
                        bs_first_ne = [x for x in bs_first
                                        if x != fundamental.empty]

                        cnt1 = len(self._first_terminals[s])
                        self._first_terminals[s].update(bs_first_ne)
                        cnt2 = len(self._first_terminals[s])

                        if cnt2 > cnt1:
                            updated = True

                        # if not all previous body symbols and bs contained
                        # empty symbol, stop adding new symbols
                        if not fundamental.empty in bs_first:
                            break

                    # if its possible to derive empty symbol from all body
                    # symbols, it's also possible to derive it from head symbol
                    if all([fundamental.empty in self._first_terminals[bs]
                            for bs in r.body_symbols]):

                        cnt1 = len(self._first_terminals[s])
                        self._first_terminals[s].add(fundamental.empty)
                        cnt2 = len(self._first_terminals[s])

                        if cnt2 > cnt1:
                            updated = True

    def _calculate_follow_terminals(self):
        self._follow_terminals = {}
        self._follow_terminals[self._start_symbol] = set([fundamental.end])
        updated = True
        while updated:
            updated = False
            for r in self._rules:
                hs = r.head_symbol
                for i, bs in enumerate(r.body_symbols):
                    self._follow_terminals.setdefault(bs, set([]))
                    #search all body symbols to the right of bs
                    for next_bs in r.body_symbols[(i + 1):]:

                        next_bs_first = self.first_terminals(next_bs)
                        next_bs_first_ne = [x for x in next_bs_first
                                        if x != fundamental.empty]

                        cnt1 = len(self._follow_terminals[bs])
                        self._follow_terminals[bs].update(next_bs_first_ne)
                        cnt2 = len(self._follow_terminals[bs])
                        if cnt2 > cnt1:
                            updated = True

                        # continue looping only if empty symbol
                        # is derivable from next_bs
                        if not fundamental.empty in next_bs_first:
                            break

                self._follow_terminals.setdefault(hs, set([]))
                #search all body symbols from the end to the beginning
                hs_follow = self._follow_terminals[hs]
                for bs in reversed(r.body_symbols):
                    bs_first = self.first_terminals(bs)

                    cnt1 = len(self._follow_terminals[bs])
                    self._follow_terminals[bs].update(hs_follow)
                    cnt2 = len(self._follow_terminals[bs])
                    if cnt2 > cnt1:
                        updated = True

                    # continue looping only if empty symbol
                    # is derivable from bs
                    if not fundamental.empty in bs_first:
                        break

    def rules_for_symbol(self, nonterm_symbol):
        return tuple((r for r in self._rules
                        if r.head_symbol == nonterm_symbol))

    def first_terminals(self, symbol):
        return self._first_terminals[symbol]

    def follow_terminals(self, nonterm_symbol):
        return self._follow_terminals[nonterm_symbol]


class CFGExtended(CFG):
    """ context-free grammar enriched with reductions """
    def __init__(self, nonterm_symbols, term_symbols, reductions,
                start_symbol):
        rules = tuple((reduction.rule for reduction in reductions))
        super(CFGExtended, self).__init__(nonterm_symbols, term_symbols,
                                            rules, start_symbol)
        self._reductions = tuple(reductions)
