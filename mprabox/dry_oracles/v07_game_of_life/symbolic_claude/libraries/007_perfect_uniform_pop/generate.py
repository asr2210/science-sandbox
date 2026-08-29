"""Experiment 007: Perfectly uniform population per position.

Each position has EXACTLY 12500 of each char {0,1,2,3} across the 50k sequences.
Achieved by per-column shuffling of [0]*12500 + [1]*12500 + [2]*12500 + [3]*12500.

Tests whether Poisson noise in uniform random hurts: if perfect uniformity beats
random uniform, then noise is the issue.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 19

rng = np.random.default_rng(SEED)

mat = np.empty((N, L), dtype=np.uint8)
# Build one column at a time so each column has exactly 12500 of each char
base_col = np.concatenate([np.full(N // 4, c, dtype=np.uint8) for c in range(4)])
assert len(base_col) == N

for p in range(L):
    col = base_col.copy()
    rng.shuffle(col)
    mat[:, p] = col

# Verify
for p in range(L):
    counts = np.bincount(mat[:, p], minlength=4)
    assert (counts == N // 4).all(), f"Position {p} has counts {counts}"
print("Per-position counts verified: exactly 12500 each char at every position.")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in mat:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} sequences with perfect per-position uniformity to {out_path}")
