"""Exp 003: per-sequence varied compositions via Dirichlet(0.5).

Each of 50,000 sequences uses its own composition drawn from a sparse
Dirichlet, so many sequences are heavily skewed toward one or two characters.

This produces strong between-sequence variance along the composition axis,
which should boost correlation if predictors care about composition.
"""
import os
import random
import numpy as np

np.random.seed(20260602)
random.seed(20260602)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]

# Dirichlet with concentration 0.5 — sparser/skewed compositions
alpha = np.full(4, 0.5)
comps = np.random.dirichlet(alpha, size=N)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        p = comps[i]
        seq_chars = np.random.choice(ALPHA, size=L, p=p)
        f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences with Dirichlet(0.5) varied compositions")
