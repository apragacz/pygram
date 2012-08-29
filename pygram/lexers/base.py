from abc import ABCMeta, abstractmethod


class Lexer(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def tokenize_file(self, f):
        pass

    @abstractmethod
    def tokenize_string(self, text):
        pass
