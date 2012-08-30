import re
from cStringIO import StringIO

from ..core.exceptions import UnknownTokenError
from ..core.locations import FileLocation
from ..core.tokens import Token


class Lexer(object):

    def __init__(self, token_config):
        self._token_config = tuple([(symbol, re.compile(pattern))
                                    for symbol, pattern in token_config])
        self._whitespace_regexp = re.compile('[ \t\r\n]*')

    def tokenize_line(self, line, line_number=None, filename=None, column_number=0):
        whitespace_re = self._whitespace_regexp
        line = line.rstrip()
        while line:
            m = whitespace_re.match(line)
            column_number += m.end()
            line = line[m.end():]
            token = None
            for symbol, regexp in self._token_config:
                m = regexp.match(line)
                if m:
                    value = line[:m.end()]
                    column_number += m.end()
                    line = line[m.end():]
                    location = FileLocation(filename,
                                            line_number,
                                            column_number,
                                            line_number,
                                            column_number + len(value))
                    token = Token(symbol=symbol, value=value, location=location)
                    break
            if token:
                yield token
            else:
                location = FileLocation(filename,
                                        line_number,
                                        column_number)
                raise UnknownTokenError(location=location)

    def tokenize_file(self, f, filename=None):

        for line_number, line in enumerate(f):

            line = line.rstrip()
            if not line:
                #omit empty lines
                continue

            for token in self.tokenize_line(line,
                                            line_number=line_number,
                                            filename=filename):
                yield token

    def tokenize_string(self, text, filename=None):
        for token in self.tokenize_file(StringIO(text), filename):
            yield token
