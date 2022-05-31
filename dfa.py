# Single state of automata
class State:
    def __init__(self, alphabet, id_list, id, terminal_id):
        self.id = id
        self.id_set = set(id_list)
        self.transitions = dict()
        self.final = terminal_id in self.id_set
        # stransitions by chars are stored in dictionaries
        for char in alphabet:
            self.transitions[char] = {}


# Deterministic Finite Automaton
class DFA:
    def __init__(self, tree, alphabet):
        self.tree = tree
        self.alphabet = alphabet
        self.count = 1
        # states of the DFA
        self.states = []
        self.terminal = tree.count - 1
        self.build_dfa()

    # Build the DFA from syntax tree
    def build_dfa(self):
        first_state = State(self.alphabet, self.tree.root.firstpos,
                            self.sequence(), self.terminal)
        self.states.append(first_state)

        temp_states = [first_state]

        # transitions to all states
        while len(temp_states) > 0:
            # take the first state (if there was no 0 the last state would be taken)
            first_state = temp_states.pop(0)
            states_list = self.transition(first_state, self.tree)

            for state in states_list:
                temp_state = State(self.alphabet, state,
                                   self.sequence(), self.terminal)
                self.states.append(temp_state)
                temp_states.append(temp_state)

    # Return counter and increment it
    def sequence(self):
        i = self.count
        self.count += 1
        return i

    # Find transitions from state using the given alphabet
    def transition(self, state, tree):
        temp_states = []

        for i in state.id_set:
            if i == self.terminal:
                continue
            label = tree.leaves[i]
            if bool(state.transitions[label]) == False:
                state.transitions[label] = tree.followpos[i]
            else:
                state.transitions[label] = state.transitions[label] | tree.followpos[i]

        for char in self.alphabet:
            if bool(state.transitions[char]) == True:
                is_new = True
                for s in self.states:
                    if s.id_set == state.transitions[char] or state.transitions[char] in temp_states:
                        is_new = False
                if is_new:
                    temp_states.append(state.transitions[char])

        return temp_states

    # Print DFA
    def print_dfa(self):
        self.format_states()

        string = '\033[92mTRANSITION TABLE:\033[0m\n'
        string += '      STATE   '
        for char in self.alphabet:
            string += '  ' + char + ' '

        for state in self.states:
            if state.id == 1:
                string += '\nBEGIN '
            else:
                string += '      '

            string += str(state.id) + '      '

            for char in self.alphabet:
                string += ' | ' + \
                    str(state.transitions[char])
            if state.final:
                string += ' | FINAL\n'
            else:
                string += ' | \n'

        print(string)

    # Format states
    def format_states(self):
        none_states = False
        for state in self.states:
            for char in self.alphabet:
                if bool(state.transitions[char]) == False:
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
