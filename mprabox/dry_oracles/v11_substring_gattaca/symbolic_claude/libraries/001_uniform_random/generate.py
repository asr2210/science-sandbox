"""Baseline: 50,000 uniformly random sequences over {0,1,2,3} of length 200."""
import os
import random

random.seed(42)

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50000
L = 200
ALPHA = "0123"

with open(OUT, "w") as f:
    for _ in range(N):
        s = "".join(random.choice(ALPHA) for _ in range(L))
        f.write(s + "\n")

print(f"wrote {N} sequences of length {L} to {OUT}")
