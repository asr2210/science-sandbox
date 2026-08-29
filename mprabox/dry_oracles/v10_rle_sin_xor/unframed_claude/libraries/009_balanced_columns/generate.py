"""Experiment 009: per-position perfectly-balanced uniform 50% GC.

Each column (1..200) contains exactly 12,500 A, 12,500 C, 12,500 G, 12,500 T
across the 50,000 sequences (instead of Binomial(50000, 0.25) per nucleotide).
Tests whether removing per-position sampling noise pushes mean_r higher.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(9)

# For each column, build a shuffled vector with exactly N/4 of each nt.
matrix = np.empty((N, L), dtype=np.int8)
base_vec = np.repeat(np.arange(4, dtype=np.int8), N // 4)  # [0]*12500 + [1]*12500 + ...
for j in range(L):
    perm = rng.permutation(N)
    matrix[:, j] = base_vec[perm]

seqs = ["".join(ALPHABET[row]) for row in matrix]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")

# stats
gc_lib = sum((s.count("C") + s.count("G")) for s in seqs[:2000]) / (2000 * L)
print(f"library GC (first 2000): {gc_lib:.4f}")
# per-position A counts (should all be 12500)
col0 = matrix[:, 0]
print(f"col 0 counts: A={np.sum(col0==0)} C={np.sum(col0==1)} G={np.sum(col0==2)} T={np.sum(col0==3)}")
print(f"wrote {len(seqs)} sequences to {OUT}")
