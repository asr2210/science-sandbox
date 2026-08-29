#!/usr/bin/env python3
"""Each sequence = random permutation of 50 of each base.

Tests if enforcing exact per-sequence base balance helps b or c.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
PER_BASE = L // 4  # 50 of each

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        bases = list("0" * PER_BASE + "1" * PER_BASE + "2" * PER_BASE + "3" * PER_BASE)
        random.shuffle(bases)
        f.write("".join(bases) + "\n")

print(f"Wrote {N} permutations (exact 50/50/50/50) to {out_path}")
