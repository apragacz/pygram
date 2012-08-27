from unittest import TestCase

from pygram.grammars.cfg import CFGExtended, CFGRule
from pygram.grammars.reductions import Reduction
from pygram.grammars.symbols import SymbolSet, SymbolInstance
from pygram.parsers.base import LRParser
from pygram.parsers.states.slr import SLRStateGenerator


class ParsersTestCase(TestCase):

    def test_exp_slr(self):

        t = SymbolSet('t', [
            ('bra_open', '('),
            ('bra_close', ')'),
            ('add', '+'),
            ('mul', '*'),
            'id',
        ])

        nt = SymbolSet('nt', [
            ('value', 'V'),
            ('exp', 'E'),
            ('product', 'P'),
            ('start', 'S'),
        ])

        rules = [
            CFGRule(nt.value, (t.id,)),
            CFGRule(nt.value, (t.bra_open, nt.exp, t.bra_close)),
            CFGRule(nt.product, (nt.value,)),
            CFGRule(nt.product, (nt.product, t.mul, nt.value)),
            CFGRule(nt.exp, (nt.product,)),
            CFGRule(nt.exp, (nt.exp, t.add, nt.product)),
            CFGRule(nt.start, (nt.exp,)),
        ]

        identity = lambda x: x

        reductions = [
            Reduction(rules[0], lambda x1: float(x1)),
            Reduction(rules[1], lambda x1, x2, x3: x2),
            Reduction(rules[2], identity),
            Reduction(rules[3], lambda x1, x2, x3: x1 * x3),
            Reduction(rules[4], identity),
            Reduction(rules[5], lambda x1, x2, x3: x1 + x3),
            Reduction(rules[6], identity),
        ]

        cfgex = CFGExtended(nt, t, reductions, nt.start)
        gen = SLRStateGenerator(cfgex)
        action_table, transition_table = gen.generate_tables()
        parser = LRParser(action_table, transition_table, initial_state=0)
        symbol_instances = [
            SymbolInstance(t.bra_open),
            SymbolInstance(t.id, 1),
            SymbolInstance(t.bra_close),
        ]
        parser.parse(symbol_instances)
