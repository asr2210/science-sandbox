"""Exp 022: Explicit uniform GRID on 4-simplex.

Instead of sampling Dir(α) (which clusters around the center), enumerate
compositions on a regular lattice over the simplex and ensure even coverage.
Each seq gets exact counts from a lattice point + random arrangement.

Goal: maximize simplex coverage to break 0.078 ceiling.
"""
import os, numpy as np
from itertools import product

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(105)
chars = np.array(list("0123"))

# Enumerate compositions (c0, c1, c2, c3) summing to L with step size GRID.
# Step ≈ 5 gives a manageable count, divide L=200 → 40 lattice points per axis
# Compositions of L into 4 nonneg ints with step 5 = C(43,3) ~ 12K. Good!
GRID = 5
# Generate lattice points: c_i = GRID * k_i where sum(k_i) = L/GRID = 40
M = L // GRID
points = []
for a in range(M + 1):
    for b in range(M + 1 - a):
        for c in range(M + 1 - a - b):
            d = M - a - b - c
            points.append((a*GRID, b*GRID, c*GRID, d*GRID))
points = np.array(points)  # shape (P, 4) summing to L
P = len(points)
print(f"lattice has {P} compositions")

# Sample N compositions WITH REPLACEMENT uniformly from lattice
idx = rng.integers(0, P, size=N)
compositions = points[idx]

lines = []
for i in range(N):
    c = compositions[i]
    base = np.concatenate([np.full(c[k], k, dtype=np.int8) for k in range(4)])
    rng.shuffle(base)
    lines.append("".join(chars[base]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} uniform-simplex-grid seqs")
