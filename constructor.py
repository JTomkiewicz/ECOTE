class Node:
    def __init__(self, id, substrar, substrildren):
        self.id = id
        self.substrar = substrar
        self.substrildren = substrildren


class SyntaxTree:
    def __init__(self):
        self.nodes = []

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


def find_nth_occur(string: str, substr: str, n: int) -> int:
    occur = 0
    n = n + 1

    for i in range(len(string)):
        if string[i] == substr:
            occur += 1

        if occur == n:
            return i

    return -1
