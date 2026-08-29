"""Exp 016: 3-control-point piecewise linear gradient.

Each sequence has 3 control compositions at positions 0, 100, 199, drawn
from Dirichlet(0.5). Composition at each position interpolates linearly
between the two nearest controls.

Tests whether richer positional structure (start/mid/end) beats simple
two-endpoint gradient.
"""
import os
import numpy as np

np.random.seed(20260615)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

# Piecewise linear weights: positions 0..99 interpolate c0->c1, 100..199 c1->c2.
left_t = np.linspace(0.0, 1.0, L // 2).reshape(-1, 1)
right_t = np.linspace(0.0, 1.0, L - L // 2).reshape(-1, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c0 = np.random.dirichlet(np.full(K, 0.5), size=N)
    c1 = np.random.dirichlet(np.full(K, 0.5), size=N)
    c2 = np.random.dirichlet(np.full(K, 0.5), size=N)
    for i in range(N):
        left = (1.0 - left_t) * c0[i] + left_t * c1[i]
        right = (1.0 - right_t) * c1[i] + right_t * c2[i]
        comps = np.vstack([left, right])  # (L, K)
        u = np.random.random(L)
        cdf = np.cumsum(comps, axis=1)
        idx = (u[:, None] < cdf).argmax(axis=1)
        f.write("".join(ALPHA[idx]) + "\n")
print(f"wrote {N} 3-control-point gradient sequences")
