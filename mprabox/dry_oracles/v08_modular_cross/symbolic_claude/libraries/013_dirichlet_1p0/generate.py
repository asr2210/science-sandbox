"""Pure Dirichlet(1.0) compositions — uniform on the 4-simplex."""
import numpy as np
import os

SEED = 131
N = 50000
L = 200
ALPHA = "0123"
ALPHA_DIR = 1.0

rng = np.random.default_rng(SEED)
probs = rng.dirichlet(np.full(4, ALPHA_DIR), size=N)

arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    arr[i] = rng.choice(4, size=L, p=probs[i])

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} Dirichlet(1.0) sequences to {out_path}")
