"""Experiment 007: iid random with different seed.

Verify that uniform random ~0.42 is consistent across seeds.
Same as 001 but seed=1234567.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(1234567)

arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
