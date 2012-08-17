from .symbols import SymbolInstance


class Reduction(object):
    def __init__(self, rule, callback=None):
        self._rule = rule
        self._callback = callback

    @property
    def rule(self):
        return self._rule

    def reduce_instances(self, symbol_instances):
        assert(len(symbol_instances) == len(self._rule.body_symbols))
        assert(all([si.symbol == bs for si, bs in zip(symbol_instances,
                                                self._rule.body_symbols)]))
        value = self._callback(*[si.value for si in symbol_instances])
        return SymbolInstance(symbol=self._rule.head_symbol, value=value)

    def __unicode__(self):
        r'%s with reduction callback %s' (unicode(self._rule, self._callback))
