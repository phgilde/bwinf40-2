import cProfile
from itertools import combinations
import pstats
import progressbar


def bitstring_to_int(string):
    result = 0
    for i in range(len(string)):
        if string[i] == "1":
            result += 2**i
    return result


def sidewise_xor(combination):
    result = 0
    for card in combination:
        result ^= card
    return result


def main():
    try:
        with open(input("Pfad: ")) as f:
            n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
            card_strings = []
            while line := f.readline():
                card_strings.append(line.strip())

        cards = [bitstring_to_int(string) for string in card_strings]
        card_remaps = {bitstring_to_int(string): string for string in card_strings}

        for combination in progressbar.progressbar(combinations(cards, n_opening_cards + 1)):
            result = sidewise_xor(combination)
            if result == 0:
                print("\n".join(["  ".join(card_remaps[card]) for card in list(combination)]))
                break
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

    cProfile.run("main()", "restats")

    p = pstats.Stats("restats")
    p.strip_dirs().sort_stats("time").print_stats(10)