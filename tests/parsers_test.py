from unittest import TestCase

from pygram.core.reductions import Reduction
from pygram.core.symbols import SymbolSet
from pygram.core.tokens import Token
from pygram.grammars.cfg import CFGExtended, CFGRule
from pygram.parsers.lr import LRParser
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
        action_table, transition_table, debug_info = gen.generate_tables()
        parser = LRParser(action_table, transition_table, initial_state=0,
                            debug_info=debug_info)

        self.dump_action_table(action_table, debug_info)

        tokens = [
            Token(t.bra_open),
            Token(t.id, 1),
            Token(t.bra_close),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, 1)

        tokens = [
            Token(t.id, 2),
            Token(t.add),
            Token(t.id, 2),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, 4)

        tokens = [
            Token(t.id, 2),
            Token(t.add),
            Token(t.id, 2),
            Token(t.mul),
            Token(t.id, 2),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, 6)

        tokens = [
            Token(t.id, 2),
            Token(t.add),
            Token(t.bra_open),
            Token(t.id, 2),
            Token(t.mul),
            Token(t.id, 2),
            Token(t.bra_close),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, 6)

        tokens = [
            Token(t.bra_open),
            Token(t.id, 2),
            Token(t.add),
            Token(t.id, 2),
            Token(t.bra_close),
            Token(t.mul),
            Token(t.id, 2),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, 8)

        tokens = [
            Token(t.bra_open),
            Token(t.bra_open),
            Token(t.id, 2),
            Token(t.add),
            Token(t.id, 3),
            Token(t.bra_close),
            Token(t.mul),
            Token(t.bra_open),
            Token(t.id, 7),
            Token(t.add),
            Token(t.id, 11),
            Token(t.bra_close),
            Token(t.bra_close),
        ]
        result = parser.parse(tokens)

        self.assertEqual(result, (2 + 3) * (7 + 11))

    def dump_action_table(self, action_table, debug_info):
        for state, actions in action_table.iteritems():
            print 'state %s (%s):' % (state, debug_info[state])
            for symbol, action in actions.iteritems():
                if action[0] >= 0:
                    if action[1]:
                        print '  %s: shift to %s' % (symbol, action[1])
                    else:
                        print '  %s: reduce using %s' % (symbol, unicode(action[2].rule))
