"""Fixed composition (25% each char) but structural variation across the 50k seqs.

Tests if ANY non-compositional feature affects eval_01. Each sequence has exactly
50 of each character (0,1,2,3), so composition is identical. Differences are pure
permutations / structural arrangements.

Variation: each seq drawn from a different random permutation of the multiset.
"""
import numpy as np
import os

SEED = 313
N = 50000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)

# Each sequence is a permutation of (50x0, 50x1, 50x2, 50x3)
base = np.concatenate([np.full(L // 4, c, dtype=np.uint8) for c in range(4)])
arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    arr[i] = rng.permutation(base)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} fixed-composition permutation sequences to {out_path}")
