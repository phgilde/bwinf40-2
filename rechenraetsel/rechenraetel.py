from random import randint, choice
from itertools import product
from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE


def calculate(term: list) -> int:
    term = list(term)
    i = 0
    while i < len(term):
        if term[i] == "*":
            term[i - 1] = term[i - 1] * term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        if term[i] == ":":
            term[i - 1] = term[i - 1] / term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        i += 1

    i = 0
    while i < len(term):
        if term[i] == "+":
            term[i - 1] = term[i - 1] + term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        if term[i] == "-":
            term[i - 1] = term[i - 1] - term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        i += 1
    return term[0]


def string_to_term(s: str) -> list:
    return [int(c) if c.isdigit() else c for c in s]


def is_calculatable(term: list) -> bool:
    term = list(term)
    i = 0
    while i < len(term):
        if term[i] == "*":
            term[i - 1] = term[i - 1] * term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        if term[i] == ":":
            term[i - 1] = term[i - 1] / term[i + 1]
            if term[i - 1] != int(term[i - 1]):
                return False
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        i += 1

    i = 0
    while i < len(term):
        if term[i] == "+":
            term[i - 1] = term[i - 1] + term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        if term[i] == "-":
            term[i - 1] = term[i - 1] - term[i + 1]
            term.pop(i)
            term.pop(i)
            i -= 2
            continue
        i += 1
    return term[0] > 0


def flatten(list_):
    return [item for sublist in list_ for item in sublist]


def is_ambiguous(term):
    length = (len(term) + 1) // 2
    for v in product(*["+-*:" for i in range(length - 1)]):
        alt_term = flatten(
            [(term[i], v[i // 2]) for i in range(0, (length - 1) * 2, 2)]
        ) + [term[-1]]
        if term == alt_term:
            continue
        if not is_calculatable(alt_term):
            continue
        if calculate(alt_term) == calculate(term):
            return True
    return False


length = int(input("Länge: "))

while (
    not is_calculatable(
        term := flatten(
            [(randint(1, 9), choice("+-*:")) for i in range(length)]
        )[:-1]
    )
) or is_ambiguous(term):
    print("failed...")
print(term)
print(calculate(term))
