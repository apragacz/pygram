class LocationError(Exception):

    def get_message(self):
        pass

    def __init__(self, location=None, value=None, msg=None):
        if not msg:
            msg = self.get_message()
        if location:
            filename = location.filename or '<Unknown>'
            line = location.line_number
            column = location.column_number
            message = '%s in file: %s, at line: %s, column %s' % (msg,
                                                            filename,
                                                            line,
                                                            column)
        else:
            message = msg
        super(LocationError, self).__init__(message)


class PygramSyntaxError(LocationError):
    pass


class LexerError(PygramSyntaxError):
    pass


class BadIndentationError(LexerError):

    def get_message(self):
        return 'Bad indentation'


class UnknownTokenError(LexerError):

    def get_message(self):
        return 'Unknown token'


class MissingOpeningBraceError(LexerError):

    def get_message(self):
        return 'Missing opening brace'


class ParserError(PygramSyntaxError):
    pass


class NoParserActionError(ParserError):

    def get_message(self):
        return 'No parser action'
