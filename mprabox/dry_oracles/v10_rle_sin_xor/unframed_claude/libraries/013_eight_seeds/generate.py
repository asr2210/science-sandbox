"""Experiment 013: 8 seeds of per-col-balanced uniform 50% GC."""
import os
import numpy as np

DIR = os.path.dirname(__file__)
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

def per_col_balanced(seed):
    rng = np.random.default_rng(seed)
    base_vec = np.repeat(np.arange(4, dtype=np.int8), N // 4)
    matrix = np.empty((N, L), dtype=np.int8)
    for j in range(L):
        matrix[:, j] = base_vec[rng.permutation(N)]
    return ["".join(ALPHABET[row]) for row in matrix]

seeds = [101, 202, 303, 404, 505, 606, 707, 808]
for k, seed in enumerate(seeds):
    out = os.path.join(DIR, f"sequences_{k}.txt")
    seqs = per_col_balanced(seed)
    with open(out, "w") as f:
        f.write("\n".join(seqs) + "\n")
    print(f"wrote sequences_{k}.txt (seed={seed})")
