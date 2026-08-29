"""Constrained-composition random: each sequence's per-char count must be in [45,55].
This narrows compositional variance (std per char ~3 instead of ~6.1) without zeroing it.
Tests if there's a sweet spot between uniform random (std=6.1) and exact balance (std=0)."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 45, 55
ALPHA = np.array(list("0123"))

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
n_written = 0
n_tries = 0
with open(OUT, "w") as f:
    while n_written < N:
        idx = rng.integers(0, 4, size=L)
        counts = np.bincount(idx, minlength=4)
        n_tries += 1
        if (counts >= LO).all() and (counts <= HI).all():
            f.write("".join(ALPHA[idx]) + "\n")
            n_written += 1
print(f"wrote {N} narrow-constrained sequences ({n_tries} tries, accept rate {N/n_tries:.3f})")
