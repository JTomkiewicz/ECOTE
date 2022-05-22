import re


class Node:
    def __init__(self, id, char, children) -> None:
        self.id = id
        self.char = char
        self.children = children
        pass


class SyntaxTree:
    def __init__(self) -> None:
        self.nodes = []
        pass

    def parse(self, regex):
        nr_of_brackets = regex.count('(')

        for i in reversed(range(nr_of_brackets)):
            index_begin = findNthOccur(regex, '(', i)
            index_end = findNthOccur(regex, ')', 0)

            print(regex[index_begin + 1:index_end])

            regex = regex[0:index_begin] + regex[index_end+1:]

        print(regex)
        # node = Node(1, 'a', [1])
        # self.nodes.append(node)


def findNthOccur(string, ch, N):
    occur = 0
    N = N + 1

    for i in range(len(string)):
        if (string[i] == ch):
            occur += 1
        if (occur == N):
            return i

    return -1


def is_regex_correct(regex: str) -> bool:
    open_sum = 0
    close_sum = 0

    for char in regex:
        if char == '(':
            open_sum += 1
        elif char == ')':
            close_sum += 1

        if close_sum > open_sum:
            return False

    if open_sum != close_sum:
        return False
    else:
        return True


def remove_not_supported_chars(regex: str) -> str:
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|\+]', '', regex)
    return regex


def to_dfa(regex: str):
    if not is_regex_correct(regex):
        print('Given REGEX is incorrect')
        quit()

    # construct augmented regex
    regex += '#'

    # construct syntax tree
    st = SyntaxTree()
    st.parse(regex)

    # evaluate functions
