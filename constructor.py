import re

from sympy import false


def is_regex_correct(regex: str) -> bool:
    open_sum = 0
    close_sum = 0

    for char in regex:
        if char == '(':
            open_sum += 1
        elif char == ')':
            close_sum += 1

        if close_sum > open_sum:
            return False

    if open_sum != close_sum:
        return False
    else:
        return True


def remove_not_supported_chars(regex: str) -> str:
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|\+]', '', regex)
    return regex


def to_dfa(regex: str):
    if not is_regex_correct(regex):
        print('Given REGEX is incorrect')
        quit()
