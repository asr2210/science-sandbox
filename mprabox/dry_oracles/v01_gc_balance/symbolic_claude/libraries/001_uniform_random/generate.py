"""
Experiment 001: Uniform random baseline.

50,000 strings of length 200, each character drawn iid uniform from {0,1,2,3}.
Provides the reference score we measure all other experiments against.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        f.write("".join(random.choices(ALPHA, k=L)))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
