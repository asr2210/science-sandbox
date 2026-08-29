"""Exp 011: 4-corner structured composition library.

12500 sequences per corner. Each corner concentrates ~70% mass on one
character, with 10% on each other character.

Tests whether explicit clustering at compositional corners beats unstructured
Dirichlet(2.0) — which averages across the simplex.
"""
import os
import numpy as np

np.random.seed(20260610)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]
K = 4
per_corner = N // K

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for corner in range(K):
        comp = np.full(K, 0.10)
        comp[corner] = 0.70
        for _ in range(per_corner):
            seq_chars = np.random.choice(ALPHA, size=L, p=comp)
            f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences (4 corner clusters)")
