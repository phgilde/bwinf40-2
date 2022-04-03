import cProfile
from itertools import combinations
import pstats
import progressbar
import math


def bitstring_to_int(string):
    result = 0
    for i in range(len(string)):
        if string[i] == "1":
            result += 2 ** i
    return result


def sidewise_xor(iterable):
    result = 0
    for card in iterable:
        result ^= card
    return result


def ncr(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def main():
    try:
        with open(input("Pfad: ")) as f:
            n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
            card_strings = []
            while line := f.readline():
                card_strings.append(line.strip())

        cards = [bitstring_to_int(string) for string in card_strings]
        card_remaps = {
            bitstring_to_int(string): string for string in card_strings
        }

        xor_dict_length = (n_opening_cards + 1) // 2
        xor_dict = {}
        for combination in combinations(cards, xor_dict_length):
            result = sidewise_xor(combination)
            xor_dict[result] = list(combination)

        for combination in combinations(
            cards, n_opening_cards + 1 - xor_dict_length
        ):
            result = sidewise_xor(combination)
            if result in xor_dict:
                if xor_dict[result] != list(combination):
                    print()
                    print(
                        "\n".join(
                            [
                                " ".join(card_remaps[card])
                                for card in list(combination)
                                + xor_dict[result]
                            ]
                        )
                    )
                    break

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

    cProfile.run("main()", "restats")

    p = pstats.Stats("restats")
    p.strip_dirs().sort_stats("time").print_stats(10)
