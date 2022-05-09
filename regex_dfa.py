def is_regex_correct(regex: str):
    print('1')


def to_dfa(regex: str):
    if not is_regex_correct(regex):
        print('Given REGEX is incorrect')
        quit()
