#!/usr/bin/env python3
"""25k strict + 25k (random + 1 8-mer from 200-bank). Push bank size 4x
beyond 017 (50-bank) to test K562 trend continuation.

Per-cell trend across bank sizes:
- 3-bank (014):   K562 0.852  SKNSH 0.880  mean 0.881
- 9-bank (016):   K562 0.855  SKNSH 0.871  mean 0.881
- 50-bank (017):  K562 0.862  SKNSH 0.872  mean 0.882
- 200-bank (this): ?
"""
import numpy as np
import os

SEED = 272727
N = 50_000
HALF = N // 2
L = 200
BANK_SIZE = 200
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
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (200-bank 8mer insert) to {out_path}")


if __name__ == "__main__":
    main()
