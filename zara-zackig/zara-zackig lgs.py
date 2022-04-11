from re import I
import sys
import numpy as np


def gauusian_elimination(matrix, result):
    result_matrix = np.concatenate((matrix, result.reshape(-1, 1)), axis=1)
    r = 0
    for i in range(matrix.shape[1]):
        while r + 1 < matrix.shape[1] and (not any(result_matrix[i:, r])):
            r += 1
        if not result_matrix[i, r]:
            for k in range(i + 1, matrix.shape[0]):
                if result_matrix[k, r]:
                    result_matrix[i] ^= result_matrix[k]
                    break
        for k in range(matrix.shape[0]):
            if result_matrix[k, r] and k != i:
                result_matrix[k] ^= result_matrix[i]
        r += 1
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


with open(input("Pfad: ")) as f:
    n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
    card_strings = []
    while line := f.readline():
        card_strings.append(line.strip())
cards_bool = [[bit == "1" for bit in card] for card in card_strings]
cards = np.array(cards_bool).T


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

    rref = gauusian_elimination(
        matrix, np.zeros((matrix.shape[0])).astype(bool)
    )[:, :-1]
    start = empty_row_start(rref)
    null_space = np.ndarray((null_space_size(rref), rref.shape[1]), dtype=bool)
    print(rref.astype(int))
    rref = add_free_coeffs(rref)
    for i in range(null_space.shape[0]):
        result = np.zeros(rref.shape[0], dtype=bool)
        result[i + start] = 1
        eliminated = gauusian_elimination(rref, result)
        null_space[i] = eliminated[:, -1].reshape(-1)[: rref.shape[1]]
    return null_space


null_space = null_space(cards)

print(null_space.astype(int))
