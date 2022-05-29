from syntax_tree import SyntaxTree
from dfa import DFA
import menu


def main():
    # show menu & read regex
    menu.show_menu('Convert regex to DFA')
    regex = menu.read_regex()

    # construct syntax tree
    tree = SyntaxTree(regex)

    tree.print_tree()

    # construct DFA
    dfa = DFA(tree)

    # read & check input string (optional)
    while True:
        menu.show_menu(
            'Input string to check, if it can be generated by regex')
        input_string = menu.read_input_string()


if __name__ == "__main__":
    main()
