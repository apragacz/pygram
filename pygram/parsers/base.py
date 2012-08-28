from abc import ABCMeta, abstractmethod


class Parser(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, tokens):
        pass
