"""Experiment 001: uniform random baseline.

Generate 50,000 strings of length 200 over {0,1,2,3}, each character
sampled iid uniformly. This is the null model.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}")
