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
        # versuche kippelement auf 1 zu setzen, 
        # in dem mit passender reihe XOR-t wird
        if not result_matrix[row, column]:
            for xor_row in range(row + 1, matrix.shape[0]):
                if result_matrix[xor_row, column]:
                    result_matrix[row] ^= result_matrix[xor_row]
                    break
            else:
                # falls keine andere 1 in dieser spalte,
                # mache bei nächster spalte weiter
                continue
        # XOR-e mit jeder anderen reihe, die eine 1 in der spalte hat, 
        # damit kippelement einzige 1 in dieser spalte ist
        for xor_row in range(matrix.shape[0]):
            if result_matrix[xor_row, column] and xor_row != row:
                result_matrix[xor_row] ^= result_matrix[row]
        # wenn kippelement erfolgreich erzeugt wurde,
        # gehe in nächste reihe, damit nächstes kippelement 
        # in nächster reihe ist. Wenn letzte Reihe erreicht ist,
        # breche ab.
        row += 1
        if row == matrix.shape[0]:
            break
    return result_matrix


# berechnet den nullraum der gegebenen matrix
def null_space(matrix):
    # bringe erweiterte matrix in spaltenstufenform (reduced column echelon form)
    rcef = gauss_jordan(matrix.T, np.identity(matrix.shape[1], dtype=bool)).T
    # trenne die erweiterte matrix wieder in ihre zwei teile (B und C)
    top_half = rcef[: matrix.shape[0]]
    bottom_half = rcef[matrix.shape[0] :]
    null_space = []
    # füge jede spalte von C zum nullraum hinzu, 
    # wenn ihre zugehörige spalte in B null ist
    for i in range(top_half.shape[1]):
        if not any(top_half[:, i]):
            null_space.append(bottom_half[:, i].reshape(-1))
    return np.array(null_space)


# karten einlesen
with open(input("Pfad: ")) as f:
    n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
    card_strings = []
    while line := f.readline():
        card_strings.append(line.strip())
cards_bool = [[bit == "1" for bit in card] for card in card_strings]
# cards entspricht der matrix K^T
cards = np.array(cards_bool).T

# nullraum der karten (K^T) berechnen
null_space = null_space(cards)

# überprüfung, ob alle nullvektoren korrekt sind
count_zero = 0
for null_vector in null_space:
    xor = np.zeros((cards.shape[0]), dtype=bool)
    for card in cards.T[null_vector]:
        xor ^= card
    if not any(xor):
        count_zero += 1
print(f"{count_zero}/{null_space.shape[0]} null vectors correct")

# gebe nullvektor aus, der so viele einsen hat, 
# wie es öffnungskarten + sicherungskarte gibt
null_space_int = null_space.astype(int)
for null_vector in null_space:
    if np.sum(null_vector.astype(int)) == n_opening_cards + 1:
        print("Echte Karten: ")
        print(cards.T[null_vector].astype(int))
        break
# wenn kein solcher vektor gefunden wurde, probiere
# probiere alle linearkombinationen der nullvektoren durch
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
