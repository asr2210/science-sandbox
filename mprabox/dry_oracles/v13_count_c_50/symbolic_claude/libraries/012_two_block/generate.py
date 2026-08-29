"""Exp 012: per-sequence two-block compositions.

Each sequence is two halves with independent random compositions.
- positions 0-99: composition c_left ~ Dirichlet(2.0)
- positions 100-199: composition c_right ~ Dirichlet(2.0), independent

Adds positional / within-sequence compositional variance on top of
between-sequence variance.
"""
import os
import numpy as np

np.random.seed(20260611)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]
K = 4
half = L // 2

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        c_left = np.random.dirichlet(np.full(K, 2.0))
        c_right = np.random.dirichlet(np.full(K, 2.0))
        left = np.random.choice(ALPHA, size=half, p=c_left)
        right = np.random.choice(ALPHA, size=half, p=c_right)
        f.write("".join(left) + "".join(right) + "\n")
print(f"wrote {N} two-block sequences")
