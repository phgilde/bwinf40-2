from re import I
import sys
import numpy as np
from itertools import product

# gauss-jordan-algorithmus
def gauss_jordan(matrix, result):
    # bildung der erweiterten koeffizientenmatrix
    print(matrix.shape, result.shape)
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
    return result_matrix


def add_free_coeffs(matrix):
    matrix = np.copy(matrix)
    empty_row_pos = empty_row_start(matrix)

    i, k = 0, 0
    while i < matrix.shape[1]:
        if matrix[k, i]:
            k += 1
        else:
            matrix[empty_row_pos, i] = 1
            empty_row_pos += 1
        i += 1
    return matrix


def empty_row_start(matrix):
    i = 0

    while any(matrix[i]):
        i += 1
    empty_row_pos = i
    return empty_row_pos


def null_space_size(rref_matrix):
    result = 0
    for i in range(rref_matrix.shape[1]):
        if np.sum(rref_matrix[:, i].astype(int)) != 1:
            result += 1
    return result


def null_space(matrix):
    if matrix.shape[1] > matrix.shape[0]:
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
    print(matrix.shape)
    rref = gauss_jordan(
        matrix.T, np.identity(matrix.shape[1], dtype=bool)
    ).T
    top_half = rref[:matrix.shape[0]]
    bottom_half = rref[matrix.shape[0]:]
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
for null_vector in null_space_int:
    if np.sum(null_vector) == n_opening_cards + 1:
        print(null_vector)
        break
else:
    for combination_factors in product([False, True], repeat=null_space.shape[0]):
        combination = np.zeros(null_space.shape[1], dtype=bool)
        for i, factor in enumerate(combination_factors):
            if factor:
                combination ^= null_space[i]
        if np.sum(combination.astype(int)) == n_opening_cards + 1:
            print(null_vector)
            break
