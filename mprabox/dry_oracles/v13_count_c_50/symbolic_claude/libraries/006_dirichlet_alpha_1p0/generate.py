"""Exp 006: Dirichlet(1.0) — uniform on the composition simplex.

If eval_01 > 0.3604 (alpha=0.5), the optimum is between 0.5 and infinity.
If lower, alpha=0.5 is the local peak.
"""
import os
import numpy as np

np.random.seed(20260605)

N = 50_000
L = 200
ALPHA = ["0", "1", "2", "3"]

comps = np.random.dirichlet(np.full(4, 1.0), size=N)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        seq_chars = np.random.choice(ALPHA, size=L, p=comps[i])
        f.write("".join(seq_chars) + "\n")
print(f"wrote {N} sequences with Dirichlet(1.0)")
