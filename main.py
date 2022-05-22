import consultant
import constructor


def main():
    option = consultant.show_menu()

    if option == 0:
        regex = input('Input REGEX: ')
        regex = constructor.remove_not_supported_chars(regex)
        constructor.to_dfa(regex)
    else:
        print('Test 1: (a|b)*abb')
        constructor.to_dfa('(a|b)*abb')


if __name__ == "__main__":
    main()
