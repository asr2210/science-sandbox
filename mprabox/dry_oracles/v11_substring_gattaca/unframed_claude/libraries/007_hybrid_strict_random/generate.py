#!/usr/bin/env python3
"""Hybrid library: 25,000 strict-balanced + 25,000 uniform random sequences.
Tests whether Pearson r averages between subsets or compounds non-linearly.
"""
import numpy as np
import os

SEED = 13579
N = 50_000
HALF = N // 2
L = 200
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    # strict half
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    # random half
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    seqs = np.concatenate([strict, rand], axis=0)
    # shuffle order so subsets are interleaved
    order = rng.permutation(N)
    seqs = seqs[order]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} hybrid seqs to {out_path}")

if __name__ == "__main__":
    main()
