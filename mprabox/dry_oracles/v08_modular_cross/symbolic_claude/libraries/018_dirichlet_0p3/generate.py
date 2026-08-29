"""Dirichlet(0.3) per-seq composition - between 0.1 (-0.0001) and 0.5 (+0.0030)."""
import numpy as np
import os

SEED = 233
N = 50000
L = 200
ALPHA = "0123"

rng = np.random.default_rng(SEED)
probs = rng.dirichlet(np.full(4, 0.3), size=N)
arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    arr[i] = rng.choice(4, size=L, p=probs[i])

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} Dirichlet(0.3) sequences to {out_path}")
