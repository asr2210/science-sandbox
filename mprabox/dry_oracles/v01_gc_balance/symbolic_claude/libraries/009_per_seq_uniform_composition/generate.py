"""
Experiment 009: Forced per-sequence uniform composition.

50K sequences, each a uniformly random permutation of
"0"*50 + "1"*50 + "2"*50 + "3"*50.

Per-position marginals across the library: uniform 25/25/25/25 (matches
baseline). Per-sequence composition: now EXACTLY 50/50/50/50 (matches
mean of baseline but with zero variance, whereas baseline iid has
per-seq stddev ~ sqrt(50*0.75)/200 ≈ 3% per char).

Tests whether per-sequence composition variance contributes negatively.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
PER_CHAR = 50  # 4 * 50 = 200

random.seed(20260603)

TEMPLATE = list("0" * PER_CHAR + "1" * PER_CHAR + "2" * PER_CHAR + "3" * PER_CHAR)

with open(OUT, "w") as f:
    for _ in range(N):
        random.shuffle(TEMPLATE)
        f.write("".join(TEMPLATE))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
