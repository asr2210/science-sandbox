"""
Experiment 010: Dirichlet-sampled per-sequence weights.

For each of 50K sequences:
  1. Draw a 4-vector probs from Dirichlet(alpha=10, 10, 10, 10).
  2. Sample 200 chars iid using those probs.

Mean per-position composition: uniform 25/25/25/25 (matches baseline).
Per-sequence composition variance: amplified ~2.5x vs baseline iid.

Tests whether ADDED per-sequence composition variance helps the score,
holding aggregate composition fixed at uniform.
"""
import os
import random

import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = 10.0

rng = np.random.default_rng(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        probs = rng.dirichlet([ALPHA] * 4)
        seq_ints = rng.choice(4, size=L, p=probs)
        f.write("".join(str(int(c)) for c in seq_ints))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
