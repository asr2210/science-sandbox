"""Dirichlet(alpha=0.5) compositions: 50k diverse-composition sequences.

Sample p_i ~ Dirichlet(0.5, 0.5, 0.5, 0.5), then draw L chars i.i.d. from Cat(p_i).
alpha < 1 pushes mass toward simplex corners → many sequences are near-homopolymer,
others balanced. Maximum diversity in composition across the 50k.

Tests: does composition matter? If yes, with diverse compositions we should see
M(seq) and T(seq) variance both increase; if they correlate via composition, r != 0.
"""
import numpy as np
import os

SEED = 11
N = 50000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)

probs = rng.dirichlet(np.full(4, 0.5), size=N)  # (N, 4)

# Sample each sequence
arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    arr[i] = rng.choice(4, size=L, p=probs[i])

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} dirichlet-composition sequences to {out_path}")
