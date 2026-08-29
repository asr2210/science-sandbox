"""Per-sequence varied doubly-stochastic Markov chain.

For each sequence:
  - sample random permutation P over {0,1,2,3} → permutation matrix M
  - T = alpha*M + (1-alpha)*J/4  (doubly stochastic, uniform stationary)
  - start from uniform random char, generate chain length 200
  - reject if composition not in [43,57]

Goal: keep per-position marginal uniform (so a, b features remain healthy),
add inter-sequence dinucleotide variance, hoping c (and overall) edges up.
"""
import os
import numpy as np
from itertools import permutations

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 43, 57
ALPHA = 0.5

perms = list(permutations(range(4)))  # 24 permutations
perm_mats = []
for p in perms:
    M = np.zeros((4, 4))
    for i, j in enumerate(p):
        M[i, j] = 1.0
    perm_mats.append(M)
perm_mats = np.array(perm_mats)  # (24,4,4)

J4 = np.full((4, 4), 0.25)

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))

accepted = 0
attempts = 0
with open(OUT, "w") as f:
    while accepted < N:
        attempts += 1
        M = perm_mats[rng.integers(0, 24)]
        T = ALPHA * M + (1 - ALPHA) * J4
        # Build cumulative rows for fast sampling
        Tc = np.cumsum(T, axis=1)
        seq = np.empty(L, dtype=np.int64)
        seq[0] = rng.integers(0, 4)
        u = rng.random(L)
        for t in range(1, L):
            seq[t] = np.searchsorted(Tc[seq[t-1]], u[t])
        # Check composition
        counts = np.bincount(seq, minlength=4)
        if counts.min() >= LO and counts.max() <= HI:
            f.write("".join(chars[seq]) + "\n")
            accepted += 1

print(f"wrote {N} sequences (acceptance {accepted}/{attempts} = {accepted/attempts:.3f})")
