"""Experiment 005: Markov chain self-transition gradient.

String i has self-transition probability p_self = 0.25 + 0.7*i/(N-1).
At each step, with prob p_self the char repeats; else uniform over other 3.
Starting char random.

Tests whether predictor responds to autocorrelation / run length / clumpiness.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 5

rng = np.random.default_rng(SEED)
p_selfs = np.linspace(0.25, 0.95, N).astype(np.float64)
starts = rng.integers(0, 4, size=N)

# Pre-generate Bernoulli "stay" decisions per (string, position) and
# "non-self" choice indices in {0,1,2}; map later by offsetting around `cur`.
stays = rng.random((N, L)) < p_selfs[:, None]
non_self = rng.integers(0, 3, size=(N, L), dtype=np.uint8)

out = np.empty((N, L), dtype=np.uint8)
for i in range(N):
    cur = int(starts[i])
    out[i, 0] = cur
    si = stays[i]
    ni = non_self[i]
    for j in range(1, L):
        if si[j]:
            out[i, j] = cur
        else:
            other = int(ni[j])
            if other >= cur:
                other += 1
            cur = other
            out[i, j] = cur

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Quick run-length stats
runs_first = np.sum(out[0, 1:] != out[0, :-1]) + 1
runs_last = np.sum(out[-1, 1:] != out[-1, :-1]) + 1
print(f"Wrote {N} sequences. First-string runs: {runs_first}, last-string runs: {runs_last}")
