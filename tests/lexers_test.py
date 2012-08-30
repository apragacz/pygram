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
        self.assertEqual(len(tokens), len(token_specs))

        for token, (symbol, value) in zip(tokens, token_specs):
            self.assertEqual(token.symbol, symbol)
            if value is not None:
                self.assertEqual(token.value, value)

    def test_expr(self):
        t = self.expr_t
        lexer = Lexer(self.expr_token_config)

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

        self.assertRaises(UnknownTokenError,
                            lambda: list(lexer.tokenize_string('(a+1)')))

    def test_expr_indented(self):
        t = self.expr_t
        special = self.special
        lexer = IndentingLexer(self.expr_token_config,
                                special.indent, special.dedent, special.newline,
                                brace_symbols=((t.bra_open, t.bra_close),))

        tokens1 = list(lexer.tokenize_string('a\n    +b'))
        token_specs1 = [
            (t.id, 'a'),
            (special.newline, None),
            (special.indent, None),
            (t.add, '+'),
            (t.id, 'b'),
            (special.newline, None),
        ]

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

        self.assertTokenSpecEqual(tokens1, token_specs1)
        self.assertTokenSpecEqual(tokens2, token_specs2)
        self.assertTokenSpecEqual(tokens3, token_specs3)
        self.assertTokenSpecEqual(tokens4, token_specs4)

        self.assertRaises(BadIndentationError,
                        lambda: list(lexer.tokenize_string('a\n    +b\n  +c')))
        self.assertRaises(UnknownTokenError,
                            lambda: list(lexer.tokenize_string('(a+1)')))
        self.assertRaises(MissingOpeningBraceError,
                            lambda: list(lexer.tokenize_string('(a+b))')))
