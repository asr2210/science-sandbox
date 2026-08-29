"""Exp 008: Dirichlet(5.0) — compositions even closer to center."""
import os
import numpy as np

np.random.seed(20260607)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]

comps = np.random.dirichlet(np.full(4, 5.0), size=N)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        seq_chars = np.random.choice(ALPHA, size=L, p=comps[i])
        f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences with Dirichlet(5.0)")
