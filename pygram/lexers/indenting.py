import re
from collections import deque

from ..core.exceptions import BadIndentationError, MissingOpeningBraceError
from ..core.locations import FileLocation
from ..core.tokens import Token
from .base import Lexer


class IndentingLexer(Lexer):

    def __init__(self, token_config, indent_symbol, dedent_symbol, newline_symbol,
                brace_symbols=[]):
        super(IndentingLexer, self).__init__(token_config)
        self._newline_symbol = newline_symbol
        self._indent_symbol = indent_symbol
        self._dedent_symbol = dedent_symbol
        self._brace_symbols = tuple(brace_symbols)
        self._brace_open_symbols = frozenset([b_open for b_open, _ in brace_symbols])
        self._brace_close_symbols = frozenset([b_close for _, b_close in brace_symbols])

    def tokenize_file(self, f, filename=None):
        whitespace_re = self._whitespace_regexp
        brace_counter = 0
        indent_level_stack = deque()
        last_indent_level = 0
        indent_score = {
            ' ': 1,
            '\t': 4,
            '\n': 0,
            '\r': 0,
        }

        for line_number, line in enumerate(f):

            line = line.rstrip()
            if not line:
                #omit empty lines
                continue

            m = whitespace_re.match(line)
            assert(bool(m))
            assert(m.start() == 0)

            line_indent = line[:m.end()]
            line_indent_len = m.end()
            line = line[m.end():]

            if brace_counter == 0:
                indent_level = sum([indent_score[c] for c in line_indent])

                if indent_level > last_indent_level:
                    indent_level_stack.append(last_indent_level)
                    last_indent_level = indent_level
                    yield Token(self._indent_symbol)

                elif indent_level < last_indent_level:
                    stack_top_indent_level = indent_level_stack.pop()
                    if indent_level != stack_top_indent_level:
                        location = FileLocation(filename,
                                                line_number,
                                                len(line_indent))
                        raise BadIndentationError(location=location)
                    last_indent_level = indent_level
                    yield Token(self._dedent_symbol)

            for token in self.tokenize_line(line, line_number=line_number,
                                            filename=filename,
                                            column_number=line_indent_len):
                if token.symbol in self._brace_open_symbols:
                    brace_counter += 1
                elif token.symbol in self._brace_close_symbols:
                    brace_counter -= 1

                if brace_counter < 0:
                    raise MissingOpeningBraceError(location=token.location)

                yield token

            yield Token(self._newline_symbol)
