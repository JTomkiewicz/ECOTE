import re


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


def remove_not_supported_chars(regex: str) -> str:
    return re.sub('[^a-zA-Z0-9\*\(\)\|\+]', '', regex)


def is_regex_correct(regex: str) -> None:
    if len(regex.strip()) == 0:
        raise Exception('Given REGEX is empty!')

    open_sum, close_sum = 0, 0

    for char in regex:
        if char == '(':
            open_sum += 1
        elif char == ')':
            close_sum += 1

        if close_sum > open_sum:
            raise Exception(
                'Given REGEX contain closing parentheses before opening parentheses!')

    if open_sum != close_sum:
        raise Exception(
            'Given REGEX contain different number of closing and opening parentheses')


def read_regex() -> str:
    regex = input('Input REGEX: ')
    regex = remove_not_supported_chars(regex)
    is_regex_correct(regex)
    return regex
