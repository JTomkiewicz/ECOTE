import re


def show_menu(txt):  # Menu for user
    print('\nWhat would you like to do?')
    print(f'0 - {txt}\n1 - exit')

    while True:
        option = read_option()
        if option in range(2):
            break
        print('Insert 0 or 1!')

    if option == 1:
        quit()


def read_option():  # Check if given option is a integer
    while True:
        try:
            number = input('Input: ')
            number = int(number)
            break
        except ValueError:
            print('Input must be a integer!')
    return int(number)


def read_regex():  # Read regex, check if it is correct and return it with its alphabet
    regex = input('Input regex: ')
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|]', '', regex)

    print()

    alphabet = []
    for char in regex:
        if char not in alphabet and char not in ['*', '|', '(', ')', '.']:
            alphabet.append(char)

    is_regex_correct(regex, alphabet)
    regex = add_cat_symbol(regex, alphabet)
    return alphabet, regex


# Check length and if it contains proper parentheses
def is_regex_correct(regex, alphabet):
    if len(regex.strip()) == 0:
        raise Exception('Given regex is empty!')

    open_sum = close_sum = 0

    for i in range(len(regex)):
        if regex[i] == '(':
            open_sum += 1
        elif regex[i] == ')':
            close_sum += 1

        if close_sum > open_sum:
            raise Exception(
                f'\033[91mGiven regex contain closing parentheses at index {i} before opening parentheses!\033[0m')

        if regex[i] == '|':
            if regex[i-1] not in alphabet or regex[i+1] not in alphabet:
                raise Exception(
                    f'\033[91mGiven regex contain | at index {i} but it is not between two characters!\033[0m')

    if open_sum != close_sum:
        raise Exception(
            '\033[91mGiven regex contain different number of closing and opening parentheses!\033[0m')


def add_cat_rules(c1, c2, alphabet):  # Concatenation rules
    if c1 in alphabet and c2 in alphabet:
        return True
    if c1 in [')', '*'] and c2 in alphabet:
        return True
    if c1 in alphabet and c2 == '(':
        return True
    if c1 == ')' and c2 == '(':
        return True
    return False


def add_cat_symbol(regex, alphabet):  # Add cat symbol between some characters
    i = 0
    while True:
        if i == len(regex) - 1:
            break
        if add_cat_rules(regex[i], regex[i+1], alphabet):
            regex = regex[:i+1] + '.' + regex[i+1:]
            i = 0
        else:
            i += 1
    return regex


def read_input_string():  # Input string that will be checked if it can be generated by the regex
    input_string = input('Input string: ')
    return input_string
