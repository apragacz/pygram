from abc import ABCMeta, abstractmethod


class Immutable(object):

    __metaclass__ = ABCMeta

    def __ne__(self, other):
        return not (self == other)

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass
