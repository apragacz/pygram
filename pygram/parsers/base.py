class LRParser(object):

    def __init__(self, action_table, transition_table, initial_state):
        self._action_table = action_table
        self._transition_table = transition_table
        self._stack = [(None, initial_state)]

    def parse(self, symbol_instances):
        for symbol_instance in symbol_instances:
            current_state = self._stack[-1][1]
            act = self._action_table[current_state][symbol_instance.symbol]
            next_state, reduction = act
            if next_state:
                #shift
                self._stack.append((symbol_instance, next_state))
            elif reduction:
                #reduction
                reduction_len = len(reduction.rule.body_symbols)
                reduction_elems = self._stack[-reduction_len:]
                self._stack = self._stack[:-reduction_len]
                symbol_instances = [si for si, _ in reduction_elems]
                reduced_symbol_instance = reduction.reduce_instances(
                                                            symbol_instances)
                next_state = self._transition_table[current_state][
                                                reduced_symbol_instance.symbol]
                self._stack.append((reduced_symbol_instance, next_state))
            else:
                ValueError('invalid state')
