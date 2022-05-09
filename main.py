import menu
import regex_dfa


def main():
    option = menu.init()

    if option == 0:
        regex = input('Input REGEX: ')
        regex_dfa.to_dfa(regex)
    elif option == 1:
        regex = input('Input REGEX: ')
    else:
        print('Test 1: (a|b)*abb')
        regex_dfa.to_dfa('(a|b)*abb')


if __name__ == "__main__":
    main()
