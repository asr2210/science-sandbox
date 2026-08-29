#!/usr/bin/env python3
"""Random baseline: uniform {0,1,2,3} sequences of length 200."""
import random
import os

random.seed(42)

N = 50000
L = 200
ALPHABET = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        seq = "".join(random.choice(ALPHABET) for _ in range(L))
        f.write(seq + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
