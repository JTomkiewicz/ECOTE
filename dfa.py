class State:
    '''
    Single state of automaton
    '''

    def __init__(self, alphabet, id_list, id, terminal_id):
        self.id = id
        self.id_set = set(id_list)
        self.transitions = dict()
        self.final = terminal_id in self.id_set
        for char in alphabet:
            self.transitions[char] = None


class DFA:
    '''
    Deterministic Finite Automaton
    '''

    def __init__(self, tree, alphabet):
        self.states = []
        self.alphabet = alphabet
        self.id_counter = 1
        self.terminal = tree.id_counter - 1
        self.create_states(tree)

    def create_states(self, tree):
        first_state = State(self.alphabet, tree.root.firstpos,
                            self.next_id(), self.terminal)
        self.states.append(first_state)

        states = [first_state]
        # transitions to all states
        while(len(states) > 0):
            temp_state = states.pop(0)
            states_list = self.transition(temp_state, tree)
            for s in states_list:
                state = State(self.alphabet, s, self.next_id(), self.terminal)
                self.states.append(state)
                states.append(state)

    def next_id(self):
        '''
        Return counter and increment it.
        '''
        i = self.id_counter
        self.id_counter += 1
        return i

    def transition(self, state, tree):
        '''
        Find transitions from state'''
        states = []

        for i in state.id_set:
            if i == self.terminal:
                continue
            label = tree.leaves[i]
            if state.transitions[label] is None:
                state.transitions[label] = tree.followpos[i]
            else:
                state.transitions[label] = state.transitions[label] | tree.followpos[i]

        for char in self.alphabet:
            if state.transitions[char] is not None:
                new = True
                for s in self.states:
                    if s.id_set == state.transitions[char] or state.transitions[char] in states:
                        new = False
                if new:
                    states.append(state.transitions[char])

        return states
