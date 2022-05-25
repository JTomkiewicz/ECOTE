import re


def read_option() -> int:
    while True:
        try:
            number = input('Input: ')
            number = int(number)
            break
        except ValueError:
            print('Input must be a integer!')
    return int(number)


def show_menu(txt: str) -> None:
    print('What would you like to do?')
    print(f'0 - {txt}\n1 - exit')

    while True:
        option = read_option()
        if option in range(2):
            break
        print('Insert 0 or 1!')

    if option == 1:
        quit()


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
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|\+]', '', regex)
    is_regex_correct(regex)
    return regex


def read_input_string() -> str:
    input_string = input('Input string: ')
    return input_string
