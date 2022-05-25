import consultant
import constructor


def run_tests():
    print('Test 1: (a|b)*abb')


def main():
    option = consultant.show_menu()

    if option == 1:
        run_tests()
        return

    regex = consultant.read_regex()

    regex = constructor.remove_not_supported_chars(regex)

    if not constructor.is_regex_correct(regex):
        return

    # construct augmented regex
    regex += '#'

    # construct syntax tree
    st = constructor.SyntaxTree()
    st.parse(regex)


if __name__ == "__main__":
    main()
