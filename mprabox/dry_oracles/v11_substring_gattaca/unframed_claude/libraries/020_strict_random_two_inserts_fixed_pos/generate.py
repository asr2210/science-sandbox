#!/usr/bin/env python3
"""25k strict + 25k (random + 2 8-mer inserts at fixed positions, each from
a 50-entry random-8mer bank). Creates a 2D cluster grid in the random half.
Fixed positions: 50 and 142 (start of the inserts).
"""
import numpy as np
import os

SEED = 131313
N = 50_000
HALF = N // 2
L = 200
BANK_SIZE = 50
MOTIF_LEN = 8
POS_A = 50
POS_B = 142
ALPH = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(HALF):
        a = rng.integers(0, BANK_SIZE)
        b = rng.integers(0, BANK_SIZE)
        rand[i, POS_A:POS_A + MOTIF_LEN] = bank[a]
        rand[i, POS_B:POS_B + MOTIF_LEN] = bank[b]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (2 fixed-pos 8mer inserts) to {out_path}")


if __name__ == "__main__":
    main()
