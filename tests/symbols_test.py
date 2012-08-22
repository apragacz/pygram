from unittest import TestCase

from pygram.grammars.symbols import SymbolSet


class SymbolTestCase(TestCase):

    def test_simple(self):

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

        self.assertRaises(ValueError, lambda: SymbolSet('test', [()]))
        self.assertRaises(ValueError, lambda: SymbolSet('test', ['a', 'a']))

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

        self.assertEqual(rb_o, rb_o)
        self.assertEqual(rb_o, terminal_symbols['('])
        self.assertNotEqual(rb_o, rb_c)
        self.assertNotEqual(rb_o, test0)

        self.assertNotEqual(test0, nonterminal_symbols2.test0)

        self.assertEqual(len(set(ts_list + ts_list)), 6)
        self.assertEqual(len(set(list(terminal_symbols)
                                + list(terminal_symbols)
                                + list(nonterminal_symbols))), 7)

        self.assertEqual(terminal_symbols, terminal_symbols)
        self.assertNotEqual(terminal_symbols, nonterminal_symbols)

        self.assertIn(test0, test_symbols)
        self.assertNotIn(test0, terminal_symbols)

        self.assertEqual(len(terminal_symbols), 6)
        self.assertEqual(len(nonterminal_symbols), 1)

        self.assertEqual(len(set([terminal_symbols, nonterminal_symbols,
                                    nonterminal_symbols2, terminal_symbols
                                    ])), 3)

        self.assertTupleEqual(tuple(terminal_symbols), tuple(ts_list))
        self.assertListEqual(list(terminal_symbols), ts_list)
        self.assertSetEqual(set(terminal_symbols), set(ts_list))
        self.assertListEqual(list(iter(terminal_symbols)), ts_list)
