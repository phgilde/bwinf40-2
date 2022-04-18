import sys
from functools import lru_cache


class HashableArray:
    def __init__(self, vals):
        self.vals = [bool(val) for val in vals]
        self.sum = sum(vals)
        self.inverted = None
        self.hash = None

    def __invert__(self):
        if self.inverted is None:
            self.inverted = HashableArray([not val for val in self.vals])
        return self.inverted

    @lru_cache(64)
    def __and__(self, other):
        return HashableArray(
            [
                val and other_val
                for val, other_val in zip(self.vals, other.vals)
            ]
        )

    def __hash__(self):
        if self.hash is None:
            self.hash = hash(tuple(self.vals))
        return self.hash

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.vals}"

    def __eq__(self, other):
        if isinstance(other, HashableArray):
            return all(
                [
                    self_val == other_val
                    for self_val, other_val in zip(self.vals, other.vals)
                ]
            )
        return False
    
    def __getitem__(self, key):
        return self.vals[key]


# Repräsentationen der 16 Ziffer in aufsteigender Reihenfolge
number_mappings = [
    HashableArray(
        [1, 1, 1, 0, 1, 1, 1],
    ),
    HashableArray(
        [0, 0, 1, 0, 0, 1, 0],
    ),
    HashableArray(
        [1, 0, 1, 1, 1, 0, 1],
    ),
    HashableArray(
        [1, 0, 1, 1, 0, 1, 1],
    ),
    HashableArray(
        [0, 1, 1, 1, 0, 1, 0],
    ),
    HashableArray(
        [1, 1, 0, 1, 0, 1, 1],
    ),
    HashableArray(
        [1, 1, 0, 1, 1, 1, 1],
    ),
    HashableArray(
        [1, 0, 1, 1, 0, 1, 0],
    ),
    HashableArray(
        [1, 1, 1, 1, 1, 1, 1],
    ),
    HashableArray(
        [1, 1, 1, 1, 0, 1, 1],
    ),
    HashableArray(
        [1, 1, 1, 1, 1, 1, 0],
    ),
    HashableArray(
        [0, 1, 0, 1, 1, 1, 1],
    ),
    HashableArray(
        [1, 1, 0, 0, 1, 0, 1],
    ),
    HashableArray(
        [0, 0, 1, 1, 1, 1, 1],
    ),
    HashableArray(
        [1, 1, 0, 1, 1, 0, 1],
    ),
    HashableArray(
        [1, 1, 0, 1, 1, 0, 0],
    ),
]


# Hexziffern als String in aufsteigender Reihenfolge
hex_numbers = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]


def hex_repr(number):
    result = []
    result.append(
        (u"\u2588" if number[0] or number[1] else " ")
        + (u"\u2588" if number[0] else " ")
        + (u"\u2588" if number[0] or number[2] else " ")
    )
    result.append(
        (u"\u2588" if number[1] else " ")
        + (" ")
        + (u"\u2588" if number[2] else " ")
    )
    result.append(
        (u"\u2588" if number[3] or number[1] or number[4] else " ")
        + (u"\u2588" if number[3] else " ")
        + (u"\u2588" if number[3] or number[2] or number[5] else " ")
    )
    result.append(
        (u"\u2588" if number[4] else " ")
        + (" ")
        + (u"\u2588" if number[5] else " ")
    )
    result.append(
        (u"\u2588" if number[6] or number[4] else " ")
        + (u"\u2588" if number[6] else " ")
        + (u"\u2588" if number[6] or number[5] else " ")
    )
    return result


def print_hex_numbers(hex_numbers):
    digits = [hex_repr(number) for number in hex_numbers]
    for i in range(5):
        print(" ".join(digit[i] for digit in digits))


# verbindet eine liste von digits zu einer einzelnen
@lru_cache(1024)
def concat(digits):
    val_list = []
    for digit in digits:
        val_list += digit.vals
    return HashableArray(val_list)


# berechnet die anzahl an umlegungen für eine transformation
@lru_cache(1024)
def n_moves(number_old, number_new):
    return (number_old & ~number_new).sum


# berechnet die höchstmögliche anzahl an stäbchen, die nach einer transformation übrig bleiben
@lru_cache(1024)
def max_difference(digits):
    result = 0
    for digit in digits:
        result += digit.sum - 2
    return result


# berechnet die höchstmögliche anzahl an stäbchen, die für eine transformation zusätzlich benötigt werden
@lru_cache(1024)
def min_difference(digits):
    result = 0
    for digit in digits:
        result += digit.sum - 7
    return result


# difference_sum = anzahl von übrig bleibenden stäbchen
# max_moves = anzahl von stäbchen, die noch wegenommen werden dürfen
# max_moves_rev = anzahl von stäbchen, die noch hingelegt werden dürfen
@lru_cache(200_000)
def find_best(number_old, max_moves, max_moves_rev, difference_sum):
    # Wenn keine Zahl, prüfe ob vorherige Ziffern gültig sind
    if not number_old:
        if difference_sum == 0:
            return tuple(), True
        else:
            return None, False

    # Prüfung, ob Differenz mit maximierung/minimierung der differenz bei rest kompensiert werden kann
    if difference_sum < -max_difference(number_old):
        return None, False
    if difference_sum > -min_difference(number_old):
        return None, False

    # Prüfung, ob differenz mit übrigen umlegungen kompensiert werden kann
    if -difference_sum > max_moves:
        return None, False
    if difference_sum > max_moves_rev:
        return None, False

    # setze erste ziffer auf F, dann E, dann D usw.
    for i in range(16)[::-1]:
        digit_new = number_mappings[i]
        # Gib Zahl zurück, wenn umlegungslimit erreicht ist und differenz null
        if max_moves == n_moves(number_old[0], digit_new):
            if (number_old[0].sum - digit_new.sum) == -difference_sum:
                return (digit_new,) + number_old[1:], True

        # Suche weiter, wenn umlegungslimit nicht überschritten ist (beide richtungen)
        if (max_moves >= n_moves(number_old[0], digit_new)) and (
            max_moves_rev >= n_moves(digit_new, number_old[0])
        ):
            next_best, success = find_best(
                number_old[1:],
                max_moves - n_moves(number_old[0], digit_new),
                max_moves_rev - n_moves(digit_new, number_old[0]),
                difference_sum + (number_old[0].sum - digit_new.sum),
            )
            # Gib ergebnis zurück, falls vertiefung erfolgreich war
            if success:
                return (digit_new,) + next_best, True
    # Gib miserfolg zurück, wenn keine passende zahl gefunden
    return None, False



# findet einzelne umlegungen, um von einer position zu einer anderen zu kommen.
def single_moves(number_old, number_new):
    number_curr = list(number_old)
    
    print_hex_numbers(number_curr)
    moves = []
    number_new = list(number_new)
    # gehe alle segmente von number_curr durch, bis es gleich number_new ist
    while number_curr != number_new:
        for i in range(len(number_old)):
            for k in range(7):
                # falls bei dem segment ein stäbchen liegt, was im ziel dort nicht liegen soll,
                # suche einen platz für es, außer wenn es das eizige in der ziffer ist
                if (
                    number_curr[i].vals[k]
                    and not number_new[i].vals[k]
                    and number_curr[i].sum != 1
                ):
                    for l in range(len(number_old)):
                        for m in range(7):
                            if (
                                number_new[l].vals[m]
                                and not number_curr[l].vals[m]
                            ):
                                vals = number_curr[i].vals.copy()
                                vals[k] = False
                                number_curr[i] = HashableArray(vals)
                                vals = number_curr[l].vals.copy()
                                vals[m] = True
                                number_curr[l] = HashableArray(vals)
                                moves.append(((i, k), (l, m)))
                                print("->")
                                print_hex_numbers(number_curr)
                                break
                        else:
                            continue
                        break
    return moves


def main():
    # Datei einlesen
    with open(input("Pfad: ")) as f:
        number_str = f.readline().strip()
        max_moves = int(f.readline())

    print_steps = input("Schritte ausgeben? (J für ja): ") == "J"
    sys.setrecursionlimit(3000)

    # Eingegebenen String in HashableArray umwandeln
    number_parsed = tuple(
        [number_mappings[int(digit, base=16)] for digit in number_str]
    )

    # höchste umlegungszahl finden
    best, _ = find_best(number_parsed, max_moves, max_moves, 0)
    number_mappings_list = number_mappings
    best_remapped = [number_mappings_list.index(digit) for digit in best]
    print()
    print("Ursprüngliche Zahl:")
    print(number_str)
    print("Höchstmögliche Zahl:")
    print("".join([hex_numbers[number] for number in best_remapped]))
    print(f"{n_moves(concat(number_parsed), concat(best))} Umlegungen")
    print("Zwischenstände:")
    if print_steps:
        single_moves(number_parsed, best)


if __name__ == "__main__":
    main()
