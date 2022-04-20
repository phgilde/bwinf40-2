from re import I
import sys
import numpy as np
from itertools import product
from progressbar import progressbar

# gauss-jordan-algorithmus


def gauss_jordan(matrix, result):
    # bildung der erweiterten matrix
    result_matrix = np.concatenate((matrix, result), axis=1)
    row = 0
    for column in range(matrix.shape[1]):
        if not result_matrix[row, column]:
            for xor_row in range(row + 1, matrix.shape[0]):
                if result_matrix[xor_row, column]:
                    result_matrix[row] ^= result_matrix[xor_row]
                    break
            else:
                continue
        for xor_row in range(matrix.shape[0]):
            if result_matrix[xor_row, column] and xor_row != row:
                result_matrix[xor_row] ^= result_matrix[row]
        row += 1
        if row == matrix.shape[0]:
            break
    return result_matrix


def null_space(matrix):
    if matrix.shape[1] > matrix.shape[0] and False:
        matrix = np.concatenate(
            (
                matrix,
                np.zeros(
                    (matrix.shape[1] - matrix.shape[0], matrix.shape[1]),
                    dtype=bool,
                ),
            ),
            axis=0,
        )
    rref = gauss_jordan(matrix.T, np.identity(matrix.shape[1], dtype=bool)).T
    top_half = rref[: matrix.shape[0]]
    bottom_half = rref[matrix.shape[0] :]
    null_space = []
    for i in range(top_half.shape[1]):
        if not any(top_half[:, i]):
            null_space.append(bottom_half[:, i].reshape(-1))
    return np.array(null_space)


with open(input("Pfad: ")) as f:
    n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
    card_strings = []
    while line := f.readline():
        card_strings.append(line.strip())
cards_bool = [[bit == "1" for bit in card] for card in card_strings]
cards = np.array(cards_bool).T


null_space = null_space(cards)

# TODO: all combinations of null vectors of none with correct number of cards
count_zero = 0
for null_vector in null_space:
    xor = np.zeros((cards.shape[0]), dtype=bool)
    for card in cards.T[null_vector]:
        xor ^= card
    if not any(xor):
        count_zero += 1
print(f"{count_zero}/{null_space.shape[0]} null vectors correct")


null_space_int = null_space.astype(int)
for null_vector in null_space:
    if np.sum(null_vector.astype(int)) == n_opening_cards + 1:
        print("Echte Karten: ")
        print(cards.T[null_vector].astype(int))
        break
else:
    print("Kein passender Basisvektor, suche Kombination...")
    for combination_factors in progressbar(
        product([False, True], repeat=null_space.shape[0]),
        max_value=2 ** null_space.shape[0],
    ):
        combination = np.zeros(null_space.shape[1], dtype=bool)
        for i, factor in enumerate(combination_factors):
            if factor:
                combination ^= null_space[i]
        if np.sum(combination.astype(int)) == n_opening_cards + 1:
            print("Echte Karten: ")
            print(cards.T[null_vector].astype(int))
            break
