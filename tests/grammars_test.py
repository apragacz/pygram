from unittest import TestCase

from pygram.grammars.cfg import (CFG, CFGExtended, CFGRule)
from pygram.grammars.symbols import SymbolSet, SymbolInstance
from pygram.grammars.reductions import (Reduction)


class GrammarTestCase(TestCase):

    def test_simple(self):
        Rule = CFGRule

        test_symbols = SymbolSet('test', [None])
        test0 = test_symbols.test0

        s_symbols = SymbolSet('S', ['S'])
        S2 = s_symbols.S

        terminal_symbols = SymbolSet('terminal', [
            ('rb_o', '('),
            ('rb_c', ')'),
            ('cb_o', '{'),
            ('cb_c', '}'),
            ('sb_o', '['),
            ('sb_c', ']'),
        ])
        nonterminal_symbols = SymbolSet('nonterminal', ['S'])
        nonterminal_symbols2 = SymbolSet('nonterminal', ['test0'])

        rb_o = terminal_symbols.rb_o
        rb_c = terminal_symbols.rb_c
        cb_o = terminal_symbols.cb_o
        cb_c = terminal_symbols.cb_c
        sb_o = terminal_symbols.sb_o
        sb_c = terminal_symbols.sb_c

        S = nonterminal_symbols.S

        ts_list = [rb_o, rb_c, cb_o, cb_c, sb_o, sb_c]

        print nonterminal_symbols
        print repr(nonterminal_symbols2)

        self.assertEqual(unicode(test0), u'test0')
        self.assertEqual(str(test0), 'test0')
        self.assertEqual(repr(test0), 'test0')
        self.assertEqual(unicode(test_symbols), u'{test0}')
        self.assertEqual(str(test_symbols), '{test0}')
        self.assertEqual(repr(test_symbols), 'SymbolSet(test, [test0])')
        self.assertEqual(test0.codename, u'test0')
        self.assertEqual(test0.display_name, u'test0')

        self.assertEqual(rb_o.display_name, '(')

        self.assertRaises(KeyError, lambda: nonterminal_symbols['T'])
        self.assertRaises(AttributeError, lambda: nonterminal_symbols.S2)
        self.assertRaises(AttributeError, lambda: nonterminal_symbols.T)

        self.assertEqual(S, nonterminal_symbols['S'])
        self.assertEqual(S, nonterminal_symbols.S)
        self.assertNotEqual(S, 'S')
        self.assertNotEqual(S, S2)
        self.assertNotEqual(rb_o, rb_c)
        self.assertNotEqual(rb_o, test0)
        self.assertNotEqual(test0, nonterminal_symbols2.test0)

        self.assertEqual(terminal_symbols, terminal_symbols)
        self.assertNotEqual(terminal_symbols, nonterminal_symbols)

        self.assertIn(test0, test_symbols)
        self.assertNotIn(test0, terminal_symbols)

        self.assertEqual(len(terminal_symbols), 6)
        self.assertEqual(len(nonterminal_symbols), 1)

        self.assertTupleEqual(tuple(terminal_symbols), tuple(ts_list))
        self.assertListEqual(list(terminal_symbols), ts_list)
        self.assertSetEqual(set(terminal_symbols), set(ts_list))
        self.assertListEqual(list(iter(terminal_symbols)), ts_list)

        rules = [
            Rule(S, (rb_o, rb_c)),
            Rule(S, (sb_o, sb_c)),
            Rule(S, (cb_o, cb_c)),
            Rule(S, (rb_o, S, rb_c)),
            Rule(S, (sb_o, S, sb_c)),
            Rule(S, (cb_o, S, cb_c)),
            Rule(S, (S, S)),
        ]

        self.assertEqual(unicode(rules[3]), 'S -> ( S )')

        reductions = [
            Reduction(rules[0], lambda x1, x2: '()'),
            Reduction(rules[1], lambda x1, x2: '[]'),
            Reduction(rules[2], lambda x1, x2: '{}'),
            Reduction(rules[3], lambda x1, x2, x3: '(%s)' % x2),
            Reduction(rules[4], lambda x1, x2, x3: '[%s]' % x2),
            Reduction(rules[5], lambda x1, x2, x3: '{%s}' % x2),
            Reduction(rules[6], lambda x1, x2: '%s%s}' % (x1, x2)),
        ]

        cfg = CFG(nonterminal_symbols, terminal_symbols, rules, S)
        cfgex = CFGExtended(nonterminal_symbols, terminal_symbols,
                            reductions, S)

        symbol_instances1 = [
            SymbolInstance(rb_o),
            SymbolInstance(S, '[]'),
            SymbolInstance(rb_c)
        ]

        si1 = reductions[3].reduce_instances(symbol_instances1)
        self.assertEqual(si1.symbol, S)
        self.assertEqual(si1.value, '([])')

        symbol_instances2 = [
            SymbolInstance(sb_o),
            si1,
            SymbolInstance(sb_c)
        ]

        si2 = reductions[4].reduce_instances(symbol_instances2)
        self.assertEqual(si2.symbol, S)
        self.assertEqual(si2.value, '[([])]')

        self.assertSetEqual(cfg.first_terminals(rb_o), set([rb_o]))
        self.assertSetEqual(cfg.first_terminals(rb_c), set([rb_c]))
        self.assertSetEqual(cfg.first_terminals(S), set([rb_o, cb_o, sb_o]))
