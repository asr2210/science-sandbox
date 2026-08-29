#!/usr/bin/env python3
"""25k strict + 25k (random + TWO 8-mer inserts at RANDOM positions, each
from a 50-bank). Tests whether random-position 2-inserts (vs 020's fixed
positions) work better — and whether 2 inserts at random positions help
(vs 017's single insert).
"""
import numpy as np
import os

SEED = 242424
N = 50_000
HALF = N // 2
L = 200
BANK_SIZE = 50
MOTIF_LEN = 8
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
        # Two inserts at random non-overlapping positions
        positions = rng.choice(L - MOTIF_LEN + 1, size=2, replace=False)
        for p in positions:
            mi = rng.integers(0, BANK_SIZE)
            rand[i, p:p + MOTIF_LEN] = bank[mi]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (2 random-pos 8mer inserts) to {out_path}")


if __name__ == "__main__":
    main()
