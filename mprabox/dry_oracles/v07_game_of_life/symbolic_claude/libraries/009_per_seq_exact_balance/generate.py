"""Experiment 009: Per-sequence EXACT balance.

Each of 50k sequences is a permutation of 50 '0's + 50 '1's + 50 '2's + 50 '3's.
So each sequence has exactly 25% of each char (no Poisson noise per sequence).

Per-position population: ~25% each char (with Poisson noise across the 50k random
permutations).

Both per-position AND per-sequence are uniform; per-sequence is EXACTLY uniform.

Tests if exact per-sequence balance beats Poisson per-seq balance (random uniform).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 29

assert L % 4 == 0, "Need L divisible by 4 for exact balance"
base = np.concatenate([np.full(L // 4, c, dtype=np.uint8) for c in range(4)])

rng = np.random.default_rng(SEED)
mat = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    perm = base.copy()
    rng.shuffle(perm)
    mat[i] = perm

# Verify
sample_counts = np.bincount(mat[0], minlength=4)
assert (sample_counts == 50).all(), f"Sample 0 counts {sample_counts}"

# Per-position verification (should have all 4 chars across 50k)
for p in range(L):
    counts = np.bincount(mat[:, p], minlength=4)
    assert (counts > 0).all(), f"Position {p} missing char: {counts}"
print(f"Per-seq counts (sample 0): {sample_counts}")
print(f"Per-pos counts (pos 0): {np.bincount(mat[:, 0], minlength=4)}")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in mat:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} per-seq-exactly-balanced sequences to {out_path}")
