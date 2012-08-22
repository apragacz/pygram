from unittest import TestCase

from pygram.grammars.cfg import (CFG, CFGExtended, CFGRule)
from pygram.grammars.symbols import SymbolSet, SymbolInstance
from pygram.grammars.reductions import (Reduction)


class GrammarTestCase(TestCase):

    def test_simple(self):

        terminal_symbols = SymbolSet('terminal', [
            ('rb_o', '('),
            ('rb_c', ')'),
            ('cb_o', '{'),
            ('cb_c', '}'),
            ('sb_o', '['),
            ('sb_c', ']'),
        ])
        nonterminal_symbols = SymbolSet('nonterminal', ['S'])

        rb_o = terminal_symbols.rb_o
        rb_c = terminal_symbols.rb_c
        cb_o = terminal_symbols.cb_o
        cb_c = terminal_symbols.cb_c
        sb_o = terminal_symbols.sb_o
        sb_c = terminal_symbols.sb_c

        S = nonterminal_symbols.S

        rules = [
            CFGRule(S, (rb_o, rb_c)),
            CFGRule(S, (sb_o, sb_c)),
            CFGRule(S, (cb_o, cb_c)),
            CFGRule(S, (rb_o, S, rb_c)),
            CFGRule(S, (sb_o, S, sb_c)),
            CFGRule(S, (cb_o, S, cb_c)),
            CFGRule(S, (S, S)),
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
