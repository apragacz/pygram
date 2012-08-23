from pygram.core.states import AtomState, MultiState


class SLRSituationState(AtomState):
    def __init__(self, head_symbol, body_previous_symbols, body_next_symbols):
        self._head_symbol = head_symbol
        self._body_previous_symbols = tuple(body_previous_symbols)
        self._body_next_symbols = tuple(body_next_symbols)

    def next_state(self, action):
        if self._body_next_symbols and self._body_next_symbols[0] == action:
            return SLRSituationState(self._head_symbol,
                                        self._body_previous_symbols + (action,),
                                        self._body_next_symbols[1:])
        else:
            return None

    @property
    def actions(self):
        if self._body_next_symbols:
            return frozenset([self._body_next_symbols[0]])
        else:
            return frozenset([])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._head_symbol != other._head_symbol:
            return False
        if self._body_previous_symbols != other._body_previous_symbols:
            return False
        if self._body_next_symbols != other._body_next_symbols:
            return False
        return True

    def __hash__(self):
        h = hash(self._head_symbol)
        h += hash(self._body_previous_symbols)
        h += hash(self._body_next_symbols)
        return h

    def show(self, fun):
        prev_sym_str = ' '.join([fun(bs)
                                    for bs in self._body_previous_symbols])
        next_sym_str = ' '.join([fun(bs)
                                    for bs in self._body_next_symbols])
        return '%s -> %s' % (fun(self._head_symbol),
                    ' '.join(filter(None, [prev_sym_str, "(@)", next_sym_str])))

    def __unicode__(self):
        return self.show(unicode)

    def __str__(self):
        return self.show(str)

    def __repr__(self):
        return self.show(repr)

    @property
    def body_next_symbols(self):
        return self._body_next_symbols


class SLRState(MultiState):

    def __init__(self, cf_grammar, atom_states):
        self._cfg = cf_grammar
        super(SLRState, self).__init__(atom_states)

    def equivalent_states(self, atom_state):
        body_next_symbols = atom_state.body_next_symbols
        eq_states = []
        if body_next_symbols:
            next_bs = body_next_symbols[0]
            for r in self._cfg.rules:
                if r.head_symbol == next_bs:
                    eq_states.append(SLRSituationState(r.head_symbol,
                                            (), r.body_symbols))
        return eq_states

    def constructor(self, atom_states):
        return self.__class__(self._cfg, atom_states)

    @property
    def actions(self):
        result = set()
        for s in self._atom_states:
            result.update(s.actions)
        return frozenset(result)


def generate_parser_states(grammar):
    pass
