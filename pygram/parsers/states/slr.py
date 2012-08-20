from pygram.core.states import AtomState


class SLRAtomState(AtomState):
    def __init__(self, head_symbol, body_previous_symbols, body_next_symbols):
        self._head_symbol = head_symbol
        self._body_previous_symbols = tuple(body_previous_symbols)
        self._body_next_symbols = tuple(body_next_symbols)

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

    def __unicode__(self):
        prev_sym_str = u' '.join([unicode(bs)
                                    for bs in self._body_previous_symbols])
        next_sym_str = u' '.join([unicode(bs)
                                    for bs in self._body_next_symbols])
        return u'%s -> %s  *  %s' % (unicode(self._head_symbol),
                                        prev_sym_str, next_sym_str)


def generate_parser_states(grammar):
    pass
