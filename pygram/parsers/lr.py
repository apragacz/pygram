from collections import deque

from ..core.symbols import fundamental
from ..core.tokens import Token
from .base import Parser


class LRParser(Parser):

    def __init__(self, action_table, transition_table, initial_state=1,
                debug_info=None):
        self._action_table = action_table
        self._transition_table = transition_table
        self._stack = deque([(None, initial_state)])
        self._debug_info = debug_info or {}

    def parse(self, tokens):
        next_symbol_instances = deque(tokens)
        #adding artificial end token
        next_symbol_instances.append(Token(symbol=fundamental.end))
        action_table = self._action_table
        transition_table = self._transition_table
        stack = self._stack

        def stack_top():
            try:
                return reversed(stack).next()
            except StopIteration:
                raise IndexError('empty parser stack')

        def next_symbol_instances_topleft():
            try:
                return iter(next_symbol_instances).next()
            except StopIteration:
                raise IndexError('all symbol instances processed')

        while next_symbol_instances:
            current_state = stack_top()[1]
            next_symbol_instance = next_symbol_instances_topleft()
            next_symbol = next_symbol_instance.symbol
            if next_symbol not in action_table[current_state]:
                raise ValueError('undefined action for state %d,'
                                ' symbol %s' % (current_state, next_symbol))
            action = action_table[current_state][next_symbol]
            if not action or len(action) != 3:
                raise ValueError('invalid action %s for state %d,'
                                ' symbol %s' % (action, current_state, next_symbol))
            code, next_state, reduction = action
            if code < 0:
                if self._debug_info:
                    mstate = self._debug_info.get(current_state, None)
                    raise ValueError('invalid state, error code %d'
                                    ' at state %s' % (-code, mstate))
                else:
                    raise ValueError('invalid state, error code %d' % (-code))
            if next_state:
                #shift
                stack.append((next_symbol_instance, next_state))
                next_symbol_instances.popleft()
            elif reduction:
                #reduction
                reduction_len = len(reduction.rule.body_symbols)
                rev_reduction_elems = []
                for _ in xrange(reduction_len):
                    rev_reduction_elems.append(stack.pop())

                #updating current state
                current_state = stack_top()[1]

                symbol_instances = [si for si, _ in reversed(rev_reduction_elems)]
                reduced_symbol_instance = reduction.reduce_instances(
                                                            symbol_instances)

                if code > 0:
                    #success! parsing ended, return reduced value
                    return reduced_symbol_instance.value

                reduced_symbol = reduced_symbol_instance.symbol
                next_state = transition_table[current_state][reduced_symbol]
                stack.append((reduced_symbol_instance, next_state))
            else:
                raise ValueError('invalid state, neither shift nor reduction defined')

        raise ValueError('invalid state, parser gone out of control scope')
