from abc import ABCMeta, abstractmethod


class Immutable(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass
