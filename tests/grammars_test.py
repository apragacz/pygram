from unittest import TestCase

from pygram.grammars.cfg import (ContextFreeGrammar,
    ContextFreeGrammarProcessor, ContextFreeGrammarRule)
from pygram.grammars.symbols import SymbolSet
from pygram.grammars.reductions import (Reduction)


class GrammarTestCase(TestCase):

    def test_simple(self):
        Rule = ContextFreeGrammarRule

        terminal_symbols = SymbolSet('terminal')
        nonterminal_symbols = SymbolSet('nonterminal')

        rb_o = terminal_symbols.new_symbol('(')
        rb_c = terminal_symbols.new_symbol(')')
        cb_o = terminal_symbols.new_symbol('{')
        cb_c = terminal_symbols.new_symbol('}')
        sb_o = terminal_symbols.new_symbol('[')
        sb_c = terminal_symbols.new_symbol(']')

        S = nonterminal_symbols.new_symbol('S')

        rules = [
            Rule(S, (rb_o, rb_c)),
            Rule(S, (sb_o, sb_c)),
            Rule(S, (cb_o, cb_c)),
            Rule(S, (rb_o, S, rb_c)),
            Rule(S, (sb_o, S, sb_c)),
            Rule(S, (cb_o, S, cb_c)),
            Rule(S, (S, S)),
        ]

        g = ContextFreeGrammar(nonterminal_symbols, terminal_symbols, rules, S)


