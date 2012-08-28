from unittest import TestCase

from pygram.grammars.cfg import CFG, CFGRule
from pygram.core.symbols import SymbolSet
from pygram.parsers.states.slr import (SLRState, SLRSituationState,
    SLRStateGenerator)


class ParserStatesTestCase(TestCase):

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

        cfg = CFG(nt, t, rules, nt.start)

        start_rule = rules[6]

        start_situation = SLRSituationState(start_rule.head_symbol,
                                            (), start_rule.body_symbols)

        s0 = SLRState(cfg, [start_situation])

        cmp1_s0 = SLRState(cfg, [
            SLRSituationState(nt.start, (), (nt.exp,)),
            SLRSituationState(nt.exp, (), (nt.exp, t.add, nt.product)),
            SLRSituationState(nt.exp, (), (nt.product,)),
            SLRSituationState(nt.product, (), (nt.product, t.mul, nt.value)),
            SLRSituationState(nt.product, (), (nt.value,)),
            SLRSituationState(nt.value, (), (t.bra_open, nt.exp, t.bra_close)),
            SLRSituationState(nt.value, (), (t.id,)),
        ])
        cmp2_s0 = SLRState(cfg, [
            SLRSituationState(nt.start, (), (nt.exp,)),
            SLRSituationState(nt.exp, (nt.exp,), (t.add, nt.product)),
        ])

        self.assertEqual(s0, cmp1_s0)
        self.assertNotEqual(s0, cmp2_s0)

        self.assertEqual(repr(s0)[:len('SLRState([')], 'SLRState([')

        self.assertEqual(unicode(str(s0)), unicode(s0))

        self.assertSetEqual(s0.actions, frozenset([
            nt.exp, nt.product, nt.value,
            t.id, t.bra_open
        ]))

        for a in s0.actions:
            next_states = s0.next_states(a)
            self.assertEqual(len(next_states), 1)

        gen = SLRStateGenerator(cfg)
        gen.generate_tables()
