#!/usr/bin/env python3
"""25k strict + 25k random, but BOTH halves get 1 8-mer inserted from the
same 50-entry random-8mer bank. Tests if cluster structure in both halves
helps or hurts.
"""
import numpy as np
import os

SEED = 121212
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
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        rand[i, start:start + MOTIF_LEN] = bank[mi]
        mi2 = rng.integers(0, BANK_SIZE)
        start2 = rng.integers(0, L - MOTIF_LEN + 1)
        strict[i, start2:start2 + MOTIF_LEN] = bank[mi2]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (insert in both halves) to {out_path}")


if __name__ == "__main__":
    main()
