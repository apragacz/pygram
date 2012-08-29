import re
from collections import deque
from cStringIO import StringIO

from .exceptions import LexerIndentationError
from .base import Lexer


class IndentingLexer(Lexer):

    def __init__(self, token_config, newline_symbol, indent_symbol, dedent_symbol,
                brace_symbols=[]):
        self._token_config = tuple([(symbol, re.compile(pattern))
                                    for symbol, pattern in token_config])
        self._newline_symbol = newline_symbol
        self._indent_symbol = indent_symbol
        self._dedent_symbol = dedent_symbol
        self._brace_symbols = tuple(brace_symbols)
        self._brace_open_symbols = tuple([b_open for b_open, _ in brace_symbols])
        self._brace_close_symbols = tuple([b_close for _, b_close in brace_symbols])
        self._whitespace_regexp = re.compile('[ \t]*')

    def tokenize_file(self, f):
        whitespace_re = self._whitespace_regexp
        brace_counter = 0
        indent_level_stack = deque()
        last_indent_level = 0
        indent_score = {
            ' ': 1,
            '\t': 4,
        }
        for line in f:
            if not line:
                #EOF
                break
            line = line.rstrip()
            if not line:
                #omit empty lines
                continue
            m = whitespace_re.match(line)
            assert(bool(m))
            assert(m.start() == 0)

            indent_level = sum([indent_score[c] for c in line[:m.end()]])

            if indent_level > last_indent_level:
                indent_level_stack.append(last_indent_level)
                last_indent_level = indent_level
                yield self._indent_symbol
            elif indent_level < last_indent_level:
                stack_top_indent_level = indent_level_stack.pop()
                if indent_level != stack_top_indent_level:
                    raise LexerIndentationError()

            line = line[m.end():]

            #TODO: match tokens

    def tokenize_string(self, text):
        self.tokenize_file(StringIO(text))
