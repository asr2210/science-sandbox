"""Experiment 004: exact uniform composition per sequence.

Each sequence has exactly 50 of each character {0,1,2,3} in random order.
Tests whether enforcing strict per-sequence balance beats iid uniform random.
"""
import numpy as np

N = 50_000
L = 200
assert L % 4 == 0
per = L // 4

rng = np.random.default_rng(7)

base = np.concatenate([np.full(per, c, dtype=np.uint8) for c in range(4)])

with open("sequences_0.txt", "w") as f:
    for _ in range(N):
        perm = rng.permutation(base)
        f.write("".join(chr(48 + c) for c in perm))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
