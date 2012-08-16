class LRParser(object):

    def __init__(self, action_table, transition_table, initial_state):
        self._action_table = action_table
        self._transition_table = transition_table
        self._stack = [initial_state]

    def parse(self, symbols):
        for symbol in symbols:
            current_state = self._stack[-1]
            act = self._action_table[current_state][symbol.type]
            if act[0]:
                #shift
                self._stack.append(symbol)
                self._stack.append(act[0])
            else:
                #reduction
                #TODO:
                pass
