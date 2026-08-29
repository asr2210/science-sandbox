#!/usr/bin/env python3
"""Random uniform seed=100, seed search continues."""
import random
import os

random.seed(100)

N = 50000
L = 200
ALPHABET = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choice(ALPHABET) for _ in range(L)) + "\n")

print(f"Wrote {N} sequences seed=100 to {out_path}")
