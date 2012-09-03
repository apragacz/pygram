from unittest import TestCase

from pygram.core.base import Immutable

from pygram.core.states import State, DeterministicState, MultiState
from pygram.parsers.base import Parser


class AbstractBaseClassesTestCase(TestCase):

    def test_immutable(self):
        Immutable.__hash__.im_func(None)
        Immutable.__eq__.im_func(None, None)

        State.next_states.im_func(None, None)
        State.actions.getter.__call__(None)
        DeterministicState.next_state.im_func(None, None)
        MultiState.equivalent_states.im_func(None, None)
        try:
            MultiState.constructor.im_func(None, [])
        except TypeError:
            pass

        Parser.parse.im_func(None, None)
