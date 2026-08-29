#!/usr/bin/env python3
"""Random uniform with seed=43 to gauge scoring noise vs experiment 001 (seed=42)."""
import random
import os

random.seed(43)

N = 50000
L = 200
ALPHABET = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        seq = "".join(random.choice(ALPHABET) for _ in range(L))
        f.write(seq + "\n")

print(f"Wrote {N} sequences seed=43 to {out_path}")
