"""Experiment 025: per-adjacent-pair balanced 50% GC.

Extends per-col balanced: in addition to each column having exactly N/4
of each base, each adjacent pair (j, j+1) has exactly N/16 of each of
the 16 dinucleotides. Built by partitioning the N rows into 4 equal
groups based on the value at column j, then within each group placing
N/16 of each base at column j+1.

This makes pair-uniform expectations exact, not just approximate.
"""
import os
import numpy as np

N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))
SEED = 12345
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)
m = np.empty((N, L), dtype=np.int8)

# Column 0: exact per-col balance (random permutation of N/4 each)
col0 = np.repeat(np.arange(4, dtype=np.int8), N // 4)
rng.shuffle(col0)
m[:, 0] = col0

# Columns 1..L-1: within each group of rows sharing the same value at
# column j-1, place exactly N/16 of each base at column j (then shuffle
# within the group). This guarantees both per-col balance AND per-pair
# balance.
sub_unit = np.repeat(np.arange(4, dtype=np.int8), N // 16)  # length N/4
for j in range(1, L):
    prev = m[:, j - 1]
    for b in range(4):
        idx = np.where(prev == b)[0]
        # idx has exactly N/4 elements; assign N/16 of each base
        perm = rng.permutation(len(idx))
        m[idx, j] = sub_unit[perm]

# Sanity checks (cheap)
for j in range(L):
    counts = np.bincount(m[:, j], minlength=4)
    assert (counts == N // 4).all(), f"col {j} unbalanced"

# Spot check pair balance on a few pairs
for j in [0, 50, 100, 199 - 1]:
    pair_counts = np.zeros((4, 4), dtype=np.int64)
    for a in range(4):
        for b in range(4):
            pair_counts[a, b] = ((m[:, j] == a) & (m[:, j + 1] == b)).sum()
    assert (pair_counts == N // 16).all(), f"pair ({j},{j+1}) unbalanced"

seqs = ["".join(ALPHABET[r]) for r in m]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}  N={N} L={L} seed={SEED}")
