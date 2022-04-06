import sys
import numpy as np
import galois


with open(input("Pfad: ")) as f:
    n_cards, n_opening_cards, n_bits = map(int, f.readline().split())
    card_strings = []
    while line := f.readline():
        card_strings.append(line.strip())
cards_bool = [[bit == "1" for bit in card] for card in card_strings]
cards = np.array(cards_bool).astype(int)

np.set_printoptions(threshold=sys.maxsize)
cards_gf2 = galois.GF(2)(cards.T)
print(cards_gf2)
null_space = cards_gf2.null_space()
print(null_space)
null_space_np = np.array(null_space)
print(null_space.shape)
null_space_corr_sum = null_space_np[
    np.sum(null_space_np, axis=1) == n_opening_cards + 1
].astype(bool)
print(np.sum(null_space_np, axis=1))
print(null_space_corr_sum)
print(cards[null_space_corr_sum[0]])
