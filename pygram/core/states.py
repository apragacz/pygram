from abc import ABCMeta, abstractmethod, abstractproperty


class State(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


class AtomState(State):

    __metaclass__ = ABCMeta


class MultiState(State):

    __metaclass__ = ABCMeta

    @abstractproperty
    def states(self):
        pass

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.states != other.states:
            return False
        return True

    def __hash__(self):
        value = sum((hash(s) for s in self.states))
        return value


def closure(states, equivalence_states_fun):
    result_states = set(states)
    q = list(states)
    while q:
        s = q.pop(0)
        eq_states = equivalence_states_fun(s)
        for eq_s in eq_states:
            if eq_s not in result_states:
                result_states.add(eq_s)
                q.append(eq_s)
    return result_states
