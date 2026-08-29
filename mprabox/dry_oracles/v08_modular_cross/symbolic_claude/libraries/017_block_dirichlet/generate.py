"""Block-structured Dirichlet: 4 blocks x 50bp per sequence, each block its own Dirichlet(0.5).

Tests if regional/positional composition variation matters beyond per-seq composition.
Each sequence has 4 distinct compositional regions; aggregate composition is mixed.
"""
import numpy as np
import os

SEED = 211
N = 50000
L = 200
N_BLOCKS = 4
BL = L // N_BLOCKS  # 50
ALPHA = "0123"

rng = np.random.default_rng(SEED)

# Per (seq, block) Dirichlet composition
probs = rng.dirichlet(np.full(4, 0.5), size=(N, N_BLOCKS))
arr = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    for b in range(N_BLOCKS):
        arr[i, b * BL : (b + 1) * BL] = rng.choice(4, size=BL, p=probs[i, b])

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(ALPHA[c] for c in row) + "\n")

print(f"Wrote {N} block-Dirichlet(0.5) sequences to {out_path}")
