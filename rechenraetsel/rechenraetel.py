import cProfile
import pstats
from random import randint, choice, seed
from itertools import product
from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
seed(42)


class NotCalculatableException(Exception):
    pass


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
        if term[i] == "/":
            term[i - 1] = term[i - 1] / term[i + 1]
            if term[i - 1] != int(term[i - 1]):
                raise NotCalculatableException
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
        if term[i] == "/":
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
    if len(term) < 3:
        return False
    for i in range(len(term))[1::2]:
        if term[i] in "+-":
            if is_ambiguous(term[:i]) or is_ambiguous(term[i + 1 :]):
                return True
    length = (len(term) + 1) // 2
    for v in product(*["+-*/" for i in range(length - 1)]):
        alt_term = flatten(
            [(term[i], v[i // 2]) for i in range(0, (length - 1) * 2, 2)]
        ) + [term[-1]]
        if term == alt_term:
            continue
        try:
            if calculate(alt_term) == calculate(term):
                return True
        except NotCalculatableException:
            pass
    return False


def main():
    try:
        length = int(input("Länge: "))

        while (
            not is_calculatable(
                term := flatten(
                    [(randint(1, 9), choice("+-*/")) for i in range(length)]
                )[:-1]
            )
        ) or is_ambiguous(term):
            pass
        print(term)
        print(calculate(term))
        print(eval("".join(str(x) for x in term)))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

    cProfile.run("main()", "restats")

    p = pstats.Stats("restats")
    p.strip_dirs().sort_stats("time").print_stats(10)
