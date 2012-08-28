class FileLocation(object):
    def __init__(self, filename=None, start_line=None, start_column=None,
                    end_line=None, end_column=None):
        self._filename = filename
        self._start_line = start_line
        self._start_column = start_column
        self._end_line = end_line
