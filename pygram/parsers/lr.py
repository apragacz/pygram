from collections import deque

from ..core.symbols import fundamental
from ..core.tokens import Token
from .base import Parser


class LRParser(Parser):

    def __init__(self, action_table, transition_table, initial_state=0,
                debug_info=None):
        self._action_table = action_table
        self._transition_table = transition_table
        self._stack = deque([(None, initial_state)])
        self._debug_info = debug_info or {}

    def parse(self, tokens):
        next_tokens = deque(tokens)
        #adding artificial end token
        next_tokens.append(Token(symbol=fundamental.end))
        action_table = self._action_table
        transition_table = self._transition_table
        stack = self._stack

        def stack_top():
            try:
                return reversed(stack).next()
            except StopIteration:
                raise IndexError('empty parser stack')

        def next_tokens_topleft():
            try:
                return iter(next_tokens).next()
            except StopIteration:
                raise IndexError('all symbol instances processed')

        while next_tokens:
            current_state = stack_top()[1]
            next_token = next_tokens_topleft()
            next_symbol = next_token.symbol
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
                stack.append((next_token, next_state))
                next_tokens.popleft()
            elif reduction:
                #reduction
                reduction_len = len(reduction.rule.body_symbols)
                rev_reduction_elems = []
                for _ in xrange(reduction_len):
                    rev_reduction_elems.append(stack.pop())

                #updating current state
                current_state = stack_top()[1]

                tokens = [si for si, _ in reversed(rev_reduction_elems)]
                reduced_token = reduction.reduce_instances(tokens)

                if code > 0:
                    #success! parsing ended, return reduced value
                    return reduced_token.value

                reduced_symbol = reduced_token.symbol
                next_state = transition_table[current_state][reduced_symbol]
                stack.append((reduced_token, next_state))
            else:
                raise ValueError('invalid state, neither shift nor reduction defined')

        raise ValueError('invalid state, parser gone out of control scope')
