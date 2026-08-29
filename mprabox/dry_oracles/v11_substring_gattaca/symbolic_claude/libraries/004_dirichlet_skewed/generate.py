"""Dirichlet-skewed compositions for higher inter-sequence compositional variance.
Each sequence draws probs from Dirichlet(alpha=0.3) over {0,1,2,3}, then samples
200 chars. Many sequences will be heavily biased toward one or two characters."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
alpha = np.array([0.3, 0.3, 0.3, 0.3])
chars = np.array(list("0123"))

probs = rng.dirichlet(alpha, size=N)  # (N, 4)
# Sample each sequence row according to its probs
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(OUT, "w") as f:
    for i in range(N):
        idx = rng.choice(4, size=L, p=probs[i])
        f.write("".join(chars[idx]) + "\n")
print(f"wrote {N} dirichlet-skewed sequences")
