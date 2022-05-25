def read_option():
    while True:
        try:
            number = input('Input: ')
            number = int(number)
            break
        except ValueError:
            print('Input must be a integer!')
    return int(number)


def show_menu():
    print('What would you like to do?')
    print('0 - convert REGEX to DFA\n1 - see some tests\n2 - exit')

    while True:
        option = read_option()
        if option in range(3):
            break
        print('Insert 0, 1 or 2!')

    if option == 2:
        quit()

    return option


def read_regex():
    regex = input('Input REGEX: ')
    return regex
