# Description

Program, crated for Compiling Techniques course, that creates directly DFA (deterministic finite automata) using syntax free for regular expression given by the user.

Program is created in python, but without any additional libraries.

To start the program type:
> python3 main.py

# Alphabet

Program reads following types of regular characters:

- [a-z]
- [A-Z]
- [0-9]

Program understands follwing meta-characters:

- **\*** means that a given symbol may appear 0 or more times
- **\|** stands for basically 'or', which means that the first or second symbol can occur
- **\()** are grouping symbols, and characters inside are treated as a single unit

Other symbols in input string will be ignored.
