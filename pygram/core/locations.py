class FileLocation(object):
    def __init__(self, filename=None,
                line_number=None,
                column_number=None,
                line_number_end=None,
                column_number_end=None):
        self._filename = filename
        self._line_number_start = line_number
        self._column_number_start = column_number
        self._line_number_end = line_number_end
        self._column_number_end = column_number_end
