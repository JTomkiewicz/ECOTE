import re


class Node:
    def __init__(self, id, substrar, substrildren) -> None:
        self.id = id
        self.substrar = substrar
        self.substrildren = substrildren
        pass


class SyntaxTree:
    def __init__(self) -> None:
        self.nodes = []
        pass

    def parse(self, regex):
        nr_of_brackets = regex.count('(')
        regex_to_slice = regex
        parts = []

        for i in reversed(range(nr_of_brackets)):
            index_begin = find_nth_occur(regex_to_slice, '(', i)
            index_end = find_nth_occur(regex_to_slice, ')', 0)

            parts.append(regex_to_slice[index_begin + 1:index_end])

            regex_to_slice = regex_to_slice[0:index_begin] + \
                regex_to_slice[index_end+1:]

        parts.append(regex_to_slice)

        print(parts)
        # node = Node(1, 'a', [1])
        # self.nodes.append(node)


def find_nth_occur(string, substr, n):
    occur = 0
    n = n + 1

    for i in range(len(string)):
        if (string[i] == substr):
            occur += 1

        if (occur == n):
            return i

    return -1


def is_regex_correct(regex: str) -> bool:
    open_sum = 0
    close_sum = 0

    for substrar in regex:
        if substrar == '(':
            open_sum += 1
        elif substrar == ')':
            close_sum += 1

        if close_sum > open_sum:
            return False

    if open_sum != close_sum:
        return False
    else:
        return True


def remove_not_supported_substrars(regex: str) -> str:
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
