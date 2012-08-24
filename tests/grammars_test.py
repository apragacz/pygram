from unittest import TestCase

from pygram.grammars.cfg import CFG, CFGExtended, CFGRule
from pygram.grammars.reductions import Reduction
from pygram.grammars.symbols import SymbolSet, SymbolInstance, fundamental


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
        self.assertEqual(len(set(rules + rules)), 7)

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

        self.assertSetEqual(set(terminal_symbols), cfg.terminal_symbols)
        self.assertSetEqual(set(nonterminal_symbols), cfg.nonterminal_symbols)

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

        self.assertSetEqual(cfgex.first_terminals(rb_o), set([rb_o]))

    def test_empty_symbol(self):

        nt = SymbolSet('nt', [
            'T',
            'S',
        ])

        rules = [
            CFGRule(nt.S, (nt.T, nt.T)),
            CFGRule(nt.T, (fundamental.empty,)),
        ]

        cfg = CFG(nt, fundamental, rules, nt.S)

        self.assertSetEqual(cfg.first_terminals(nt.S), set([fundamental.empty]))
        self.assertSetEqual(cfg.first_terminals(nt.T), set([fundamental.empty]))

    def test_exp(self):

        t = SymbolSet('t', [
            ('bra_open', '('),
            ('bra_close', ')'),
            ('add', '+'),
            ('mul', '*'),
            'id',
            'num',
        ])

        nt = SymbolSet('nt', [
            ('value', 'V'),
            ('exp', 'E'),
            ('product', 'P'),
            ('start', 'S'),
        ])

        rules = [
            CFGRule(nt.value, (t.id,)),
            CFGRule(nt.value, (t.num,)),
            CFGRule(nt.value, (t.bra_open, nt.exp, t.bra_close)),
            CFGRule(nt.product, (nt.value,)),
            CFGRule(nt.product, (nt.product, t.mul, nt.value)),
            CFGRule(nt.exp, (nt.product,)),
            CFGRule(nt.exp, (nt.exp, t.add, nt.product)),
            CFGRule(nt.start, (nt.exp,)),
        ]

        cfg = CFG(nt, t, rules, nt.start)

        first_terminals = set([t.bra_open, t.id, t.num])

        for s in nt:
            self.assertSetEqual(cfg.first_terminals(s), first_terminals)

        for s in [nt.value, nt.product]:
            self.assertSetEqual(cfg.follow_terminals(s), set([
                t.bra_close, t.add, t.mul, fundamental.end
            ]))

        self.assertSetEqual(cfg.follow_terminals(nt.exp), set([
            t.bra_close, t.add, fundamental.end
        ]))
        self.assertSetEqual(cfg.follow_terminals(nt.start), set([
            fundamental.end
        ]))

        self.assertSetEqual(cfg.follow_terminals(t.bra_open), set([
            t.id, t.num, t.bra_open
        ]))
        self.assertSetEqual(cfg.follow_terminals(t.bra_close), set([
            t.mul, t.add, fundamental.end, t.bra_close
        ]))
        self.assertSetEqual(cfg.follow_terminals(t.add), set([
            t.id, t.num, t.bra_open
        ]))
        self.assertSetEqual(cfg.follow_terminals(t.mul), set([
            t.id, t.num, t.bra_open
        ]))
        self.assertSetEqual(cfg.follow_terminals(t.id), set([
            t.mul, t.add, fundamental.end, t.bra_close
        ]))
        self.assertSetEqual(cfg.follow_terminals(t.num), set([
            t.mul, t.add, fundamental.end, t.bra_close
        ]))
