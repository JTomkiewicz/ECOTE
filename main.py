from syntax_tree import SyntaxTree
from dfa import DFA
import menu


def main():
    # show menu & read regex with its alphabet
    menu.show_menu('Convert regex to DFA')
    alphabet, regex = menu.read_regex()

    # construct & print syntax tree
    tree = SyntaxTree(regex)
    tree.print_tree()

    # construct & print DFA
    dfa = DFA(tree, alphabet)
    dfa.print_dfa()

    # read & check input string (optional)
    while True:
        menu.show_menu(
            'Input string to check, if it can be generated by regex')
        input_string = menu.read_input_string()


if __name__ == "__main__":
    main()
