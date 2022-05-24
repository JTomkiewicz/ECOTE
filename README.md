# Compiling Techniques project

## Description

The aim of this project is to write a program that will create directly DFA (deterministic finite automata) using syntax free for regular expression given by the user.

To start the program type:

> python3 main.py

## Alphabet

Program reads following types of regular characters:

- [a-z]
- [A-Z]
- [0-9]

Program understands follwing meta-characters:

- **\*** means that a given symbol may appear 0 or more times
- **\+** is similar to \*, but means that a given symbol may appear 1 or more times
- **\|** stands for basically 'or', which means that the first or second symbol can occur
- **\()** are grouping symbols, and characters inside are treated as a single unit

Other symbols in input string will be ignored.
