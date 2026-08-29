"""Exp 015: smooth gradient with Dirichlet(0.5) endpoints — more extreme."""
import os
import numpy as np

np.random.seed(20260614)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

t = np.linspace(0.0, 1.0, L).reshape(-1, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c_starts = np.random.dirichlet(np.full(K, 0.5), size=N)
    c_ends = np.random.dirichlet(np.full(K, 0.5), size=N)
    for i in range(N):
        comps = (1.0 - t) * c_starts[i] + t * c_ends[i]
        u = np.random.random(L)
        cdf = np.cumsum(comps, axis=1)
        idx = (u[:, None] < cdf).argmax(axis=1)
        f.write("".join(ALPHA[idx]) + "\n")
print(f"wrote {N} smooth-gradient sequences with Dirichlet(0.5) endpoints")
