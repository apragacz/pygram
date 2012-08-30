class LexerError(Exception):
    pass


class BadIndentationError(LexerError):
    pass


class UnknownTokenError(LexerError):
    pass
