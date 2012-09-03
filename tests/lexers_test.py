from unittest import TestCase

from pygram.core.exceptions import (UnknownTokenError, BadIndentationError,
    MissingOpeningBraceError)
from pygram.core.symbols import SymbolSet
from pygram.lexers.base import Lexer
from pygram.lexers.indenting import IndentingLexer


class LexersTestCase(TestCase):

    def setUp(self):
        self.expr_t = SymbolSet('t', [
            ('bra_open', '('),
            ('bra_close', ')'),
            ('add', '+'),
            ('mul', '*'),
            'id',
        ])
        self.special = SymbolSet('special', ('indent', 'dedent', 'newline'))
        t = self.expr_t
        self.expr_token_config = (
            (t.bra_open, '\('),
            (t.bra_close, '\)'),
            (t.add, '\+'),
            (t.mul, '\*'),
            (t.id, '[_]*[A-Za-z][A-Za-z0-9_]*'),
        )

    def assertTokenSpecEqual(self, tokens, token_specs):
        for token, (symbol, value) in zip(tokens, token_specs):
            self.assertEqual(token.symbol, symbol)
            if value is not None:
                self.assertEqual(token.value, value)

        self.assertEqual(len(tokens), len(token_specs))

    def test_expr(self):
        t = self.expr_t
        lexer = Lexer(self.expr_token_config)

        #test the same expresion: ( a + b ) with various whitespaces
        tokens1 = list(lexer.tokenize_string('(a    +   b)'))
        tokens2 = list(lexer.tokenize_string('(a\n+\nb\n)'))
        tokens3 = list(lexer.tokenize_string(' ( a+\n b )  '))
        tokens4 = list(lexer.tokenize_string('(a+b)'))
        tokens5 = list(lexer.tokenize_string('(a+\n\nb)'))
        token_specs = [
            (t.bra_open, '('),
            (t.id, 'a'),
            (t.add, '+'),
            (t.id, 'b'),
            (t.bra_close, ')'),
        ]

        self.assertTokenSpecEqual(tokens1, token_specs)
        self.assertTokenSpecEqual(tokens2, token_specs)
        self.assertTokenSpecEqual(tokens3, token_specs)
        self.assertTokenSpecEqual(tokens4, token_specs)
        self.assertTokenSpecEqual(tokens5, token_specs)

        #should fail, no token for digits specified
        self.assertRaises(UnknownTokenError,
                            lambda: list(lexer.tokenize_string('(a+1)')))

    def test_expr_indented(self):
        t = self.expr_t
        special = self.special
        lexer = IndentingLexer(self.expr_token_config,
                                special.indent, special.dedent, special.newline,
                                brace_symbols=((t.bra_open, t.bra_close),))

        #one line + one indented line
        tokens1 = list(lexer.tokenize_string('a\n    +b'))
        token_specs1 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'b'),
            (special.newline, None),
        ]

        #one line + two indented lines (same indent level)
        tokens2 = list(lexer.tokenize_string('a\n    +b\n\n    +c'))
        token_specs2 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'b'),
            (special.newline, None),
            (t.add, '+'),
            (t.id, 'c'),
            (special.newline, None),
        ]

        #one line + one indented line, continued  (using braces)
        tokens3 = list(lexer.tokenize_string('a\n    +(b\n  +c)'))
        token_specs3 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.bra_open, '('),
            (t.id, 'b'),
            (special.newline, None),
            (t.add, '+'),
            (t.id, 'c'),
            (t.bra_close, ')'),
            (special.newline, None),
        ]

        #two lines + one indented line, continued  (indent, dedent)
        tokens4 = list(lexer.tokenize_string('a\n    +b\n\n+c'))
        token_specs4 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'b'),
            (special.newline, None),
            (special.dedent, None),
            (t.add, '+'),
            (t.id, 'c'),
            (special.newline, None),
        ]

        #non-indent, two indentions (one line, two lines), continued by non indented line
        tokens5 = list(lexer.tokenize_string('a\n    +b\n\n        +c\n        \n        +d\n        \n+e'))
        token_specs5 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'b'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'c'),
            (special.newline, None),
            (t.add, '+'),
            (t.id, 'd'),
            (special.newline, None),
            (special.dedent, None),
            (special.dedent, None),
            (t.add, '+'),
            (t.id, 'e'),
            (special.newline, None),
        ]

        self.assertTokenSpecEqual(tokens1, token_specs1)
        self.assertTokenSpecEqual(tokens2, token_specs2)
        self.assertTokenSpecEqual(tokens3, token_specs3)
        self.assertTokenSpecEqual(tokens4, token_specs4)
        self.assertTokenSpecEqual(tokens5, token_specs5)

        self.assertRaises(BadIndentationError,
                        lambda: list(lexer.tokenize_string('a\n    +b\n  +c')))
        self.assertRaises(UnknownTokenError,
                            lambda: list(lexer.tokenize_string('(a+1)')))
        self.assertRaises(MissingOpeningBraceError,
                            lambda: list(lexer.tokenize_string('(a+b))')))
