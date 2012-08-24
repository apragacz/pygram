from abc import ABCMeta, abstractmethod, abstractproperty
from collections import deque

from .base import Immutable


class Action(Immutable):
    pass


class State(Immutable):

    __metaclass__ = ABCMeta

    @abstractmethod
    def next_states(self, action):
        pass

    @abstractproperty
    def actions(self):
        pass


class DeterministicState(object):

    __metaclass__ = ABCMeta

    def next_states(self, action):
        st = self.next_state(action)
        if st is None:
            return []
        else:
            return [st]

    @abstractmethod
    def next_state(self, action):
        pass


class AtomState(DeterministicState):

    __metaclass__ = ABCMeta


class MultiState(DeterministicState):

    __metaclass__ = ABCMeta

    def __init__(self, atom_states):
        self._atom_states = frozenset(self.closure(atom_states))

    @abstractmethod
    def equivalent_states(self, atom_state):
        pass

    def closure(self, atom_states):
        result_states = set(atom_states)
        q = deque(atom_states)
        while q:
            s = q.popleft()
            eq_states = self.equivalent_states(s)
            for eq_s in eq_states:
                if eq_s not in result_states:
                    result_states.add(eq_s)
                    q.append(eq_s)
        return result_states

    def constructor(self, atom_states):
        return self.__class__(atom_states)

    def next_state(self, action):
        next_atom_states = []
        for s in self._atom_states:
            next_atom_states.extend(s.next_states(action))
        return self.constructor(next_atom_states)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self._atom_states != other._atom_states:
            return False
        return True

    def __hash__(self):
        return hash(self._atom_states)

    def show(self, fun):
        return '%s([%s])' % (self.__class__.__name__,
                                ', '.join(map(fun, self._atom_states)))

    def __str__(self):
        return self.show(str)

    def __repr__(self):
        return self.show(repr)

    def __unicode__(self):
        return self.show(unicode)

