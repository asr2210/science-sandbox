"""Exp 005: Dirichlet(0.3) — between the alpha=0.5 (peak) and 0.1 (worse) points."""
import os
import numpy as np

np.random.seed(20260604)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]

alpha = np.full(4, 0.3)
comps = np.random.dirichlet(alpha, size=N)

# Mild floor to avoid degenerate all-same sequences.
comps = np.clip(comps, 0.005, None)
comps = comps / comps.sum(axis=1, keepdims=True)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        p = comps[i]
        seq_chars = np.random.choice(ALPHA, size=L, p=p)
        f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences with Dirichlet(0.3) compositions")
