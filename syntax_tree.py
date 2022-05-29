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


class SyntaxTree:
    def __init__(self):
        self.tokens = []
        self.stack = []

    def build(self, regex):
        self.create_tokens(regex)
        self.create_stack()

        self.root = Node('.', 'concat')
        self.leaves = dict()
        self.id_counter = 1

        self.build_tree()
        self.calculate_functions(self.root)

    def create_tokens(self, regex):
        temp_str = ''

        for char in regex:
            if char in ['(', ')', '|', '*', '+', '.']:
                if temp_str != '':
                    self.tokens.append(temp_str)
                    temp_str = ''
                self.tokens.append(char)
            else:
                temp_str += char

        if temp_str != '':
            self.tokens.append(temp_str)

    def create_stack(self):
        temp_stack = []

        for token in self.tokens:
            if token == '(':
                temp_stack.append(token)
            elif token == ')':
                while len(temp_stack) > 0 and temp_stack[-1] != '(':
                    self.stack.append(temp_stack.pop())
                temp_stack.pop()
            elif token == '*':
                temp_stack.append(token)
            elif token == '|':
                while len(temp_stack) > 0 and temp_stack[-1] in ['*', '.']:
                    self.stack.append(temp_stack.pop())
                temp_stack.append(token)
            elif token == '+':
                temp_stack.append(token)
            elif token == '.':
                while len(temp_stack) > 0 and temp_stack[-1] in ['*', '+']:
                    self.stack.append(temp_stack.pop())
                temp_stack.append(token)
            else:
                self.stack.append(token)

        while len(temp_stack) > 0:
            self.stack.append(temp_stack.pop())

    def build_tree(self):
        temp_stack = []

        for token in self.stack:
            if token == '.':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(
                    Node('.', 'concat', lchild=lc, rchild=rc))
            elif token == '*':
                lc = temp_stack.pop()
                temp_stack.append(Node('*', 'star', lchild=lc))
            elif token == '|':
                lc = temp_stack.pop()
                rc = temp_stack.pop()
                temp_stack.append(Node('|', 'or', lchild=lc, rchild=rc))
            elif token == '+':
                lc = temp_stack.pop()
                temp_stack.append(Node('*', 'plus', lchild=lc))
            else:
                temp_node = Node(token, 'identifier', id=self.next_id())
                self.leaves[temp_node.id] = temp_node.label
                temp_stack.append(temp_node)

        temp_node = Node('#', 'identifier', id=self.next_id())
        self.leaves[temp_node.id] = temp_node.label
        self.root.lchild = temp_stack.pop()
        self.root.rchild = temp_node

    def next_id(self):
        i = self.id_counter
        self.id_counter += 1
        return i

    def calculate_functions(self, node):
        pass
