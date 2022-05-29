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
