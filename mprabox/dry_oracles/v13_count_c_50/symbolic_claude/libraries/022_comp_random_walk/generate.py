"""Exp 022: compositional random walk per sequence.

Each sequence's per-position composition follows a random walk in the
4-simplex:
- c_0 ~ Dirichlet(0.5)
- c_t = (1 - eps) * c_{t-1} + eps * Dirichlet(0.5)  [renormalized]

Adjacent positions have nearly identical compositions, while distant positions
can diverge significantly. Smoother and more variable than 2-endpoint
linear gradient, but without Markov memory of characters.
"""
import os
import numpy as np

np.random.seed(20260621)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4
EPS = 0.05  # step size in composition space

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        # Pre-draw L random perturbations.
        perturbations = np.random.dirichlet(np.full(K, 0.5), size=L)
        # Run random walk.
        comps = np.empty((L, K))
        comps[0] = perturbations[0]
        for t in range(1, L):
            comps[t] = (1.0 - EPS) * comps[t - 1] + EPS * perturbations[t]
        # Sample each position from its own composition.
        u = np.random.random(L)
        cdf = np.cumsum(comps, axis=1)
        idx = (u[:, None] < cdf).argmax(axis=1)
        f.write("".join(ALPHA[idx]) + "\n")
print(f"wrote {N} compositional random walk sequences (eps={EPS})")
