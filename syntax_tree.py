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
            tree_string = '\n' + self.label_to_string(show_func) + '\n'
        else:
            temp_string = ''
            if not instar:
                for i in range(2):
                    for j in range(level):
                        if j in linelist:
                            temp_string += '   ' * (j != 0) + '|'
                        else:
                            temp_string += '   '

                    if i == 0:
                        temp_string += '\n'

            tree_string = temp_string + '___' + \
                self.label_to_string(show_func) + '\n' * (not star)

        if rchild:
            linelist.pop(-1)

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
        self.leaves = dict()

        # build tree without functions
        self.build_tree()

        # evaluate four functions: firstpos, lastpos, nullable, followpos
        self.followpos = [set() for _ in range(self.count)]
        # evaluate recursively starting from root
        self.calculate_functions(self.root)

    # Create tokens from input regex
    def create_tokens(self):
        temp_stack = []

        char_table = []
        for char in self.regex:
            char_table.append(char)

        for token in char_table:
            if token in ['(', '*']:
                temp_stack.append(token)
            elif token == ')':
                while len(temp_stack) > 0 and temp_stack[-1] != '(':
                    self.tokens.append(temp_stack.pop())
                temp_stack.pop()
            elif token == '|':
                while len(temp_stack) > 0 and temp_stack[-1] in ['*', '.']:
                    self.tokens.append(temp_stack.pop())
                temp_stack.append(token)
            elif token == '.':
                while len(temp_stack) > 0 and temp_stack[-1] == '*':
                    self.tokens.append(temp_stack.pop())
                temp_stack.append(token)
            else:
                self.tokens.append(token)

        while len(temp_stack) > 0:
            self.tokens.append(temp_stack.pop())

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
                self.leaves[temp_node.id] = temp_node.char
                temp_stack.append(temp_node)

        # at the end add right-hand marker #
        temp_node = Node('#', id=self.sequence())
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
            # compute followpos for star
            self.calculate_followpos(node)
        elif node.char == '.':
            node.nullable = node.lchild.nullable and node.rchild.nullable
            if node.lchild.nullable:  # firstpos
                node.firstpos = node.lchild.firstpos | node.rchild.firstpos
            else:
                node.firstpos = node.lchild.firstpos
            if node.rchild.nullable:  # lastpos
                node.lastpos = node.lchild.lastpos | node.rchild.lastpos
            else:
                node.lastpos = node.rchild.lastpos
            # conpute followpos for cat
            self.calculate_followpos(node)
        else:
            if node.char == '@':
                # when empty char
                node.nullable = True
            else:
                node.firstpos.add(node.id)
                node.lastpos.add(node.id)

    # Calculate followpos for . and *
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
        # print tree without functions
        print(self.root.print_tree())
        # print tree with functions
        print(self.root.print_tree(show_func=True))
