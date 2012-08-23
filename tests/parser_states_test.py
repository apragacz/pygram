from unittest import TestCase

from pygram.grammars.cfg import CFG, CFGExtended, CFGRule
from pygram.grammars.reductions import Reduction
from pygram.grammars.symbols import SymbolSet, SymbolInstance, fundamental
from pygram.parsers.states.slr import SLRState, SLRSituationState


class ParserStatesTestCase(TestCase):

    def test_exp(self):

        t = SymbolSet('t', [
            ('bra_open', '('),
            ('bra_close', ')'),
            ('add', '+'),
            ('mul', '*'),
            'id',
        ])

        nt = SymbolSet('nt', [
            'value',
            'exp',
            'product',
            'start',
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

        cfg = CFG(nt, t, rules, nt.start)

        start_rule = rules[6]

        start_situation = SLRSituationState(start_rule.head_symbol,
                                            (), start_rule.body_symbols)

        slr_states = set([])

        s0 = SLRState(cfg, [start_situation])

        print s0.actions

        print str(s0)
        print unicode(s0)
        print repr(s0)

        for a in s0.actions:
            print s0.next_states(a)

        self.assertEqual(1, 0)
