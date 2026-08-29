#!/usr/bin/env python3
"""Control: 25k strict + 25k (random + 1 RANDOM 8-mer per seq). Tests if the
motif lift is from biological motif content or just generic structured
8-base insertion.
"""
import numpy as np
import os

SEED = 77777
N = 50_000
HALF = N // 2
L = 200
MOTIF_LEN = 8
ALPH = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    # generate a fixed bank of random 8-mers (mimics motif basket of size 9)
    bank = rng.integers(0, 4, size=(9, MOTIF_LEN), dtype=np.int8)
    for i in range(HALF):
        mi = rng.integers(0, bank.shape[0])
        start = rng.integers(0, L - MOTIF_LEN + 1)
        rand[i, start:start + MOTIF_LEN] = bank[mi]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (control: 25k strict + 25k random+1 random-8mer) to {out_path}")


if __name__ == "__main__":
    main()
