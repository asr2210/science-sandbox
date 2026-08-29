"""Experiment 005: Dirichlet-sampled compositions.

Each sequence i gets its own composition p_i ~ Dirichlet(alpha=1)
(uniform over the 3-simplex), then iid sample length-200 from p_i.

This creates MUCH more composition variance across the library than
uniform random. Tests whether more compositional spread helps or hurts.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(2024)

# Sample one composition per sequence
alpha = np.ones(4)
comps = rng.dirichlet(alpha, size=N)  # (N, 4)

with open("sequences_0.txt", "w") as f:
    for i in range(N):
        seq = rng.choice(4, size=L, p=comps[i])
        f.write("".join(chr(48 + c) for c in seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
