from .slr import SLRSituationState, SLRState, SLRStateGenerator
from ...core.symbols import fundamental
from ...grammars.cfg import CFGRule


class LRSituationState(SLRSituationState):
    def __init__(self, head_symbol, body_previous_symbols, body_next_symbols,
                    follow_symbol):
        super(LRSituationState, self).__init__(head_symbol,
                                                body_previous_symbols,
                                                body_next_symbols)
        self._follow_symbol = follow_symbol

    def next_state(self, action):
        if self._body_next_symbols and self._body_next_symbols[0] == action:
            return LRSituationState(self._head_symbol,
                                    self._body_previous_symbols + (action,),
                                    self._body_next_symbols[1:],
                                    self._follow_symbol)
        else:
            return None

    def __eq__(self, other):
        if not super(LRSituationState, self).__eq__(other):
            return False
        if self._follow_symbol != other._follow_symbol:
            return False
        return True

    def __hash__(self):
        h = super(LRSituationState, self).__hash__()
        h += hash(self._follow_symbol)
        return h

    def show(self, fun):
        prev_sym_str = ' '.join([fun(bs)
                                    for bs in self._body_previous_symbols])
        next_sym_str = ' '.join([fun(bs)
                                    for bs in self._body_next_symbols])
        return '(%s -> %s, %s)' % (fun(self._head_symbol),
                    ' '.join(filter(None, [prev_sym_str, "#", next_sym_str])),
                    self._follow_symbol)

    @property
    def follow_symbol(self):
        return self._follow_symbol


class LRState(SLRState):

    def equivalent_states(self, atom_state):
        body_next_symbols = atom_state.body_next_symbols

        eq_states = []
        if body_next_symbols:

            first_next_symbols = set()
            for bns in body_next_symbols[1:] + (atom_state.follow_symbol,):
                bns_first = self._cfg.first_terminals(bns)
                bns_first_ne = [ft for ft in bns_first if ft != fundamental.empty]
                first_next_symbols.update(bns_first_ne)
                if fundamental.empty not in bns_first:
                    break

            next_bs = body_next_symbols[0]
            for r in self._cfg.rules:
                if r.head_symbol == next_bs:
                    for follow_symbol in first_next_symbols:
                        eq_states.append(LRSituationState(r.head_symbol,
                                                        (),
                                                        r.body_symbols,
                                                        follow_symbol))
        return eq_states

    def find_reduction_rule(self, follow_symbol):
        for situation in self._atom_states:
            #follow_terms = self._cfg.follow_terminals(situation.head_symbol)
            if (situation.body_next_symbols == ()
                    and follow_symbol == situation.follow_symbol):
                rule = CFGRule(situation.head_symbol,
                                situation.body_previous_symbols)
                return rule
        return None


class LRStateGenerator(SLRStateGenerator):

    def generate_start_state(self):
        start_rules = self._cfg.rules_for_symbol(self._cfg.start_symbol)
        start_situations = [LRSituationState(r.head_symbol, (), r.body_symbols,
                                                fundamental.end)
                            for r in start_rules]
        start_state = LRState(self._cfg, start_situations)
        return start_state
