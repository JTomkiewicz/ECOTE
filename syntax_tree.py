class Node:
    def __init__(self, type, label, id=None, lchild=None, rchild=None):
        self.type = type
        self.label = label
        self.id = id
        self.lchild = lchild
        self.rchild = rchild
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

    def label_to_string(self, char):
        if char == '.':
            return 'cat'
        if char == '*':
            return 'star'
        if char == '|':
            return 'or'
        return char

    def print_tree(self, level=0, linelist=[], rchild=False, instar=False):
        '''
        Print tree in a pretty way
        '''
        star = self.type == 'star'

        if level == 0:
            tree_string = self.label_to_string(self.label) + '\n'
        else:
            temp_string = ''
            if not instar:
                for i in range(2):
                    for j in range(level):
                        if j in linelist:
                            temp_string += '\t' * (j != 0) + '|'
                        else:
                            temp_string += '\t'

                    if i == 0:
                        temp_string += '\n'

            tree_string = temp_string + '___' + \
                self.label_to_string(self.label) + '\n' * (not star)

        if rchild:
            linelist.pop(-1)

        if self.lchild:
            tree_string += self.lchild.print_tree(level + 1, linelist +
                                                  [level] * (not star), instar=star)

        if self.rchild:
            tree_string += self.rchild.print_tree(level + 1, linelist +
                                                  [level], rchild=True)

        return tree_string


class SyntaxTree:
    def __init__(self, regex):
        self.regex = regex
        self.count = 1

        # create tokens and stack
        self.tokens = []
        self.stack = []
        self.create_tokens()
        self.create_stack()

        # root node is always catenation of # (right-hand marker) and rest of the tree
        self.root = Node('cat', '.')
        self.leaves = dict()

        # build tree without functions
        self.build_tree()

        # evaluate four functions: firstpos, lastpos, nullable, followpos
        self.followpos = [set() for _ in range(self.count)]
        self.calculate_functions(self.root)

    def create_tokens(self):
        '''
        Create tokens (list that has elements and alphabets of regex) from regex.
        '''
        temp_str = ''

        for char in self.regex:
            if char in ['(', ')', '|', '*', '.']:
                if temp_str != '':
                    self.tokens.append(temp_str)
                    temp_str = ''
                self.tokens.append(char)
            else:
                temp_str += char

        if temp_str != '':
            self.tokens.append(temp_str)

    def create_stack(self):
        '''
        Create stack from tokens that is later used to create tree.
        '''
        temp_stack = []

        for token in self.tokens:
            if token in ['(', '*']:
                temp_stack.append(token)
            elif token == ')':
                while len(temp_stack) > 0 and temp_stack[-1] != '(':
                    self.stack.append(temp_stack.pop())
                temp_stack.pop()
            elif token == '|':
                while len(temp_stack) > 0 and temp_stack[-1] in ['*', '.']:
                    self.stack.append(temp_stack.pop())
                temp_stack.append(token)
            elif token == '.':
                while len(temp_stack) > 0 and temp_stack[-1] == '*':
                    self.stack.append(temp_stack.pop())
                temp_stack.append(token)
            else:
                self.stack.append(token)

        while len(temp_stack) > 0:
            self.stack.append(temp_stack.pop())

    def build_tree(self):
        '''
        Build syntax tree at this moment without firstpos and lastpos functions.
        '''
        temp_stack = []

        for token in self.stack:
            if token == '.':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(
                    Node('cat', '.', lchild=lc, rchild=rc))
            elif token == '*':
                lc = temp_stack.pop()
                temp_stack.append(Node('star', '*', lchild=lc))
            elif token == '|':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(Node('or', '|', lchild=lc, rchild=rc))
            else:
                temp_node = Node('identifier', token, id=self.give_id())
                self.leaves[temp_node.id] = temp_node.label
                temp_stack.append(temp_node)

        # at the end add right-hand marker #
        temp_node = Node('identifier', '#', id=self.give_id())
        self.leaves[temp_node.id] = temp_node.label
        self.root.lchild = temp_stack.pop()
        self.root.rchild = temp_node

    def give_id(self):
        '''
        Return count and increment it.
        '''
        i = self.count
        self.count += 1
        return i

    def calculate_functions(self, node):
        '''
        Using recursion calculate nullable, firstpos and lastpos for each node.
        '''
        # stop recursion when node in Nullable
        if not node:
            return

        # run function for both left and right child
        self.calculate_functions(node.lchild)
        self.calculate_functions(node.rchild)

        if node.type == 'identifier':
            if node.label == '@':
                # when empty char
                node.nullable = True
            else:
                node.firstpos.add(node.id)
                node.lastpos.add(node.id)
        elif node.type == 'or':
            node.nullable = node.lchild.nullable or node.rchild.nullable
            # | is equivalent to union
            node.firstpos = node.lchild.firstpos | node.rchild.firstpos
            node.lastpos = node.lchild.lastpos | node.rchild.lastpos
        elif node.type == 'star':
            node.nullable = True
            node.firstpos = node.lchild.firstpos
            node.lastpos = node.lchild.lastpos
            # compute followpos for star
            self.calculate_followpos(node)
        elif node.type == 'cat':
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

    def calculate_followpos(self, node):
        '''
        Calculate followpos for star and cat.
        '''
        if node.type == 'cat':
            for pos in node.lchild.lastpos:
                self.followpos[pos] = self.followpos[pos] | node.rchild.firstpos
        elif node.type == 'star':
            for pos in node.lchild.lastpos:
                self.followpos[pos] = self.followpos[pos] | node.lchild.firstpos

    def print_tree(self):
        '''
        Print syntax tree starting from root.
        '''
        print(self.root.print_tree())
