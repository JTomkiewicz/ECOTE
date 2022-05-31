import re


def show_menu(txt):
    print('\nWhat would you like to do?')
    print(f'0 - {txt}\n1 - exit')

    while True:
        option = read_option()
        if option in range(2):
            break
        print('Insert 0 or 1!')

    if option == 1:
        quit()


def read_option():
    while True:
        try:
            number = input('Input: ')
            number = int(number)
            break
        except ValueError:
            print('Input must be a integer!')
    return int(number)


def read_regex():
    regex = input('Input regex: ')
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|]', '', regex)
    is_regex_correct(regex)

    print()

    alphabet = []
    for char in regex:
        if char not in alphabet and char not in ['*', '|', '(', ')', '.']:
            alphabet.append(char)

    regex = add_cat_symbol(regex, alphabet)

    return alphabet, regex


def is_regex_correct(regex):
    if len(regex.strip()) == 0:
        raise Exception('Given regex is empty!')

    open_sum, close_sum = 0, 0

    for char in regex:
        if char == '(':
            open_sum += 1
        elif char == ')':
            close_sum += 1

        if close_sum > open_sum:
            raise Exception(
                'Given regex contain closing parentheses before opening parentheses!')

    if open_sum != close_sum:
        raise Exception(
            'Given regex contain different number of closing and opening parentheses!')


def add_cat_rules(c1, c2, alphabet):
    if c1 in alphabet and c2 in alphabet:
        return True
    if c1 in [')', '*'] and c2 in alphabet:
        return True
    if c1 in alphabet and c2 == '(':
        return True
    if c1 == ')' and c2 == '(':
        return True
    return False


def add_cat_symbol(regex, alphabet):
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


def read_input_string():
    input_string = input('Input string: ')
    return input_string
