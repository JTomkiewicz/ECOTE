import re


def is_regex_correct(regex: str):
    print('1')


def remove_not_supported_chars(regex: str):
    regex = re.sub('[^a-zA-Z0-9\*\(\)\|\+]', '', regex)
    return regex


def to_dfa(regex: str):
    if not is_regex_correct(regex):
        print('Given REGEX is incorrect')
        quit()
