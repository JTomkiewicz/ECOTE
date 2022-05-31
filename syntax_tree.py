class Node:
    def __init__(self, char, id=None, lchild=None, rchild=None):
        self.char = char
        self.id = id
        self.lchild = lchild
        self.rchild = rchild
        # three functions
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = False

    # Convert symbols to strings and show functions
    def label_to_string(self, show_func):
        first_pos_string = ','.join(map(str, self.firstpos))
        last_pos_string = ','.join(map(str, self.lastpos))
        char_string = self.char

        if self.char == '.':
            char_string = 'CAT'
        elif self.char == '*':
            char_string = 'STAR'
        elif self.char == '|':
            char_string = 'OR'

        if show_func:
            return f'{char_string} first_pos({first_pos_string}) last_pos({last_pos_string})'
        return char_string

    # Print tree in a pretty way
    def print_tree(self, level=0, linelist=[], rchild=False, instar=False, show_func=False):
        star = self.char == '*'

        if level == 0:
            tree_string = self.label_to_string(show_func) + '\n'
        else:
            string = ''
            if not instar:
                for i in range(2):
                    for j in range(level):
                        if j in linelist:
                            string += '   ' * (j != 0) + '|'
                        else:
                            string += '   '

                    if i == 0:
                        string += '\n'

            tree_string = string + '___' + \
                self.label_to_string(show_func) + '\n' * (not star)

        if rchild:
            linelist.pop()

        if self.lchild:
            tree_string += self.lchild.print_tree(level + 1, linelist +
                                                  [level] * (not star), instar=star, show_func=show_func)

        if self.rchild:
            tree_string += self.rchild.print_tree(level + 1, linelist +
                                                  [level], rchild=True, show_func=show_func)

        return tree_string


class SyntaxTree:
    def __init__(self, regex):
        self.regex = regex
        self.count = 1

        # create tokens
        self.tokens = []
        self.create_tokens()

        # root node is always catenation of # (right-hand marker) and rest of the tree
        self.root = Node('.')
        # leaves are nodes that contain only chars from alphabet
        self.leaves = dict()

        # build tree without functions
        self.build_tree()

        # evaluate four functions: firstpos, lastpos, nullable, followpos
        self.followpos = [set() for _ in range(self.count)]
        # evaluate recursively starting from root
        self.calculate_functions(self.root)

    # Creates table containing chars from regex in postfix notation (operator is at the right ex. x*y is xy*)
    def create_tokens(self):
        # store regex chars in table
        char_table = []
        for char in self.regex:
            char_table.append(char)

        temp_tokens = []
        for token in char_table:
            if token in ['(', '*']:
                temp_tokens.append(token)
            elif token == ')':
                while len(temp_tokens) > 0 and temp_tokens[-1] != '(':
                    self.tokens.append(temp_tokens.pop())
                temp_tokens.pop()
            elif token == '|':
                while len(temp_tokens) > 0 and temp_tokens[-1] in ['*', '.']:
                    self.tokens.append(temp_tokens.pop())
                temp_tokens.append(token)
            elif token == '.':
                while len(temp_tokens) > 0 and temp_tokens[-1] == '*':
                    self.tokens.append(temp_tokens.pop())
                temp_tokens.append(token)
            else:
                self.tokens.append(token)

        while len(temp_tokens) > 0:
            self.tokens.append(temp_tokens.pop())

    # Build syntax tree at this moment without function evaluation
    def build_tree(self):
        temp_stack = []
        for token in self.tokens:
            if token == '.':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(
                    Node('.', lchild=lc, rchild=rc))
            elif token == '*':
                lc = temp_stack.pop()
                temp_stack.append(Node('*', lchild=lc))
            elif token == '|':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(Node('|', lchild=lc, rchild=rc))
            else:
                temp_node = Node(token, id=self.sequence())
                # nodes that contain alphabet chars are leaves
                self.leaves[temp_node.id] = temp_node.char
                temp_stack.append(temp_node)

        # at the end add right-hand marker #
        temp_node = Node('#', id=self.sequence())
        # right-hand marker is a leaf too
        self.leaves[temp_node.id] = temp_node.char
        self.root.lchild = temp_stack.pop()
        self.root.rchild = temp_node

    # Return count and increment it
    def sequence(self):
        i = self.count
        self.count += 1
        return i

    # Using recursion calculate nullable, firstpos and lastpos for each node
    def calculate_functions(self, node):
        # stop recursion
        if not node:
            return

        # run function for both left and right child
        self.calculate_functions(node.lchild)
        self.calculate_functions(node.rchild)

        if node.char == '|':
            node.nullable = node.lchild.nullable or node.rchild.nullable
            node.firstpos = node.lchild.firstpos | node.rchild.firstpos
            node.lastpos = node.lchild.lastpos | node.rchild.lastpos
        elif node.char == '*':
            node.nullable = True
            node.firstpos = node.lchild.firstpos
            node.lastpos = node.lchild.lastpos
            self.calculate_followpos(node)
        elif node.char == '.':
            node.nullable = node.lchild.nullable and node.rchild.nullable
            # firstpos
            if node.lchild.nullable:
                node.firstpos = node.lchild.firstpos | node.rchild.firstpos
            else:
                node.firstpos = node.lchild.firstpos
            # lastpos
            if node.rchild.nullable:
                node.lastpos = node.lchild.lastpos | node.rchild.lastpos
            else:
                node.lastpos = node.rchild.lastpos
            self.calculate_followpos(node)
        else:
            # leaf node labelled with position i
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)

    # Rules for followpos reffer only to cat-node and star-node
    def calculate_followpos(self, node):
        if node.char in ['.', '*']:
            for pos in node.lchild.lastpos:
                if node.char == '.':
                    firstpos_union = node.rchild.firstpos
                else:
                    firstpos_union = node.lchild.firstpos
                self.followpos[pos] = self.followpos[pos] | firstpos_union

    # Print syntax tree starting from root
    def print_tree(self):
        print('\033[92mSYNTAX TREE WITHOUT FUNCTIONS:\033[0m')
        print(self.root.print_tree())
        print('\033[92mSYNTAX TREE WITH FUNCTIONS:\033[0m')
        print(self.root.print_tree(show_func=True))
