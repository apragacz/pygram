class LRParser(object):

    def __init__(self, action_table, transition_table, initial_state):
        self._action_table = action_table
        self._transition_table = transition_table
        self._stack = [(None, initial_state)]

    def parse(self, symbol_instances):
        next_symbol_instances = list(symbol_instances)
        action_table = self._action_table
        transition_table = self._transition_table
        while next_symbol_instances:
            current_state = self._stack[-1][1]
            next_symbol_instance = next_symbol_instances[0]
            next_symbol = next_symbol_instance.symbol
            act = action_table[current_state][next_symbol]
            next_state, reduction = act
            if next_state:
                #shift
                self._stack.append((next_symbol_instance, next_state))
                next_symbol_instances.pop(0)
            elif reduction:
                #reduction
                reduction_len = len(reduction.rule.body_symbols)
                reduction_elems = self._stack[-reduction_len:]
                for _ in xrange(reduction_len):
                    self._stack.pop()
                symbol_instances = [si for si, _ in reduction_elems]
                reduced_symbol_instance = reduction.reduce_instances(
                                                            symbol_instances)
                reduced_symbol = reduced_symbol_instance.symbol
                next_state = transition_table[current_state][reduced_symbol]
                self._stack.append((reduced_symbol_instance, next_state))
            else:
                ValueError('invalid state')
