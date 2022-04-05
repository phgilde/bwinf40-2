import sys
import numpy as np


def gaussian_elimination(matrix, result):
    order_matrix = np.identity(min(matrix.shape), dtype=int)
    result_matrix = np.concatenate((matrix, result.reshape(-1, 1)), axis=1)
    for i in range(min(matrix.shape)):
        r = i
        while (
            not any(result_matrix[i : , r])
        ) and r < matrix.shape[1]:
            r += 1
        if r != i and r < matrix.shape[1]:
            (
                result_matrix[:, r],
                result_matrix[:, i],
            ) = (
                result_matrix[:, i],
                result_matrix[:, r],
            )
            order_matrix[r], order_matrix[i] = (
                order_matrix[i],
                order_matrix[r],
            )
        if not result_matrix[i, i]:
            for k in range(i + 1, matrix.shape[0]):
                if result_matrix[k, i]:
                    result_matrix[i] ^= result_matrix[k]
                    break
        for k in range(0, matrix.shape[0]):
            if result_matrix[k, i] and k != i:
                result_matrix[k] ^= result_matrix[i]
    result_matrix[: order_matrix.shape[0], : order_matrix.shape[1]] = (
        result_matrix[: order_matrix.shape[0], : order_matrix.shape[1]]
        @ order_matrix.T
    )
    return result_matrix


with open(input("Pfad: ")) as f:
    n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
    card_strings = []
    while line := f.readline():
        card_strings.append(line.strip())
cards_bool = [[bit == "1" for bit in card] for card in card_strings]
cards = np.array(cards_bool).astype(int)
if n_cards > n_bits:
    cards = np.concatenate(
        (cards, np.zeros((n_cards, n_cards - n_bits - 1), dtype=int)), axis=1
    )


for h in range(n_cards):
    solving_matrix = gaussian_elimination(
        np.delete(cards, (h), axis=0).T, cards[h]
    )
    print(solving_matrix)
    if all(solving_matrix[range(n_cards - 1), range(n_cards - 1)]):
        result = np.insert(solving_matrix[:, -1], h, 1)
        if sum(result[:n_cards]) == n_opening_cards + 1:
            xor = np.zeros_like(cards[0, :n_bits])
            for card in cards[result[:n_cards] == 1][:, :n_bits]:
                xor ^= card
                print(" ".join(map(str, card)))
                print()
            print(" ".join(map(str, xor)))
            break

