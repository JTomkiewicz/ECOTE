import consultant
import constructor


def run_tests():
    print('Test 1: (a|b)*abb')
    procedure('(a|b)*abb', True)


def procedure(regex: str, is_test: bool = False) -> None:
    # construct augmented regex
    regex += '#'

    # construct syntax tree
    st = constructor.SyntaxTree()
    st.parse(regex)


def main():
    option = consultant.show_menu()

    if option == 1:
        run_tests()
        return

    regex = consultant.read_regex()
    procedure(regex)


if __name__ == "__main__":
    main()
