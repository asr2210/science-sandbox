"""Exp 025: 25K bigram-Dir(0.3) + 25K uniform-simplex-grid.

Mix exp 010 (best on eval_01) and exp 022 (best on eval_07, eval_08).
Test if mixture captures complementary signal.
"""
import os, numpy as np
from itertools import product

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
HALF = N // 2
L = 200

rng = np.random.default_rng(131)
chars = np.array(list("0123"))

lines = []

# Half A: bigram-Dir(0.3) (exp 010 style)
for i in range(HALF):
    bw = rng.dirichlet([0.3] * 16).reshape(4, 4)
    row_sums = bw.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    P = bw / row_sums
    pi = bw.sum(axis=1)
    pi = pi / pi.sum() if pi.sum() > 0 else np.ones(4) / 4
    seq = np.empty(L, dtype=np.int8)
    seq[0] = rng.choice(4, p=pi)
    for t in range(1, L):
        seq[t] = rng.choice(4, p=P[seq[t-1]])
    lines.append("".join(chars[seq]))

# Half B: uniform-simplex-grid (exp 022 style)
GRID = 5
M = L // GRID
points = []
for a in range(M + 1):
    for b in range(M + 1 - a):
        for c in range(M + 1 - a - b):
            d = M - a - b - c
            points.append((a*GRID, b*GRID, c*GRID, d*GRID))
points = np.array(points)
idx = rng.integers(0, len(points), size=HALF)
compositions = points[idx]
for i in range(HALF):
    c = compositions[i]
    base = np.concatenate([np.full(c[k], k, dtype=np.int8) for k in range(4)])
    rng.shuffle(base)
    lines.append("".join(chars[base]))

rng.shuffle(lines)
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} mixed bigram+grid seqs")
