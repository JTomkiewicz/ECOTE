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
        self.tree = tree
        self.count = 1
        self.states = []
        self.alphabet = alphabet
        self.terminal = tree.count - 1
        self.create_states()

    def create_states(self):
        first_state = State(self.alphabet, self.tree.root.firstpos,
                            self.sequence(), self.terminal)
        self.states.append(first_state)

        states = [first_state]
        # transitions to all states
        while(len(states) > 0):
            temp_state = states.pop(0)
            states_list = self.transition(temp_state, self.tree)
            for s in states_list:
                state = State(self.alphabet, s, self.sequence(), self.terminal)
                self.states.append(state)
                states.append(state)

    def sequence(self):
        '''
        Return counter and increment it.
        '''
        i = self.count
        self.count += 1
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

    def print_dfa(self):
        '''
        Print DFA.
        '''
        self.format_states()

        ret = 'STATES\n'
        for state in self.states:
            ret += f'{state.id}: {state.id_set}\n'
        print(ret)

        ret = 'TRANSITION TABLE:\n'
        ret += '      STATE   '
        for char in self.alphabet:
            ret += '  ' + char + ' '

        for state in self.states:
            if state.id == 1:
                ret += '\nBEGIN '
            else:
                ret += '      '

            ret += str(state.id) + '      '

            for char in self.alphabet:
                ret += ' | ' + \
                    str(state.transitions[char])
            if state.final:
                ret += ' | FINAL\n'
            else:
                ret += ' | \n'

        print(ret)

    def format_states(self):
        '''
        Format states.
        '''
        none_states = False
        for state in self.states:
            for char in self.alphabet:
                if state.transitions[char] is None:
                    none_states = True
                    state.transitions[char] = self.count
                temp_transitions = state.transitions[char]
                for second_state in self.states:
                    if second_state.id_set == temp_transitions:
                        state.transitions[char] = second_state.id

        if none_states:
            self.states.append(
                State(self.alphabet, [], self.count, self.terminal))
            for char in self.alphabet:
                self.states[-1].transitions[char] = self.states[-1].id
