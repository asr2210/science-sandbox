#!/usr/bin/env python3
"""Random uniform seed=7."""
import random
import os

random.seed(7)
N, L = 50000, 200
ALPHABET = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choice(ALPHABET) for _ in range(L)) + "\n")
print(f"Wrote {N} sequences seed=7")
