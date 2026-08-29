"""Experiment 021: Peak finding — slightly stronger '0' bias.

p = (0.325, 0.225, 0.225, 0.225). Between exp 011 (0.30) and exp 015 (0.40).
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.325, 0.225, 0.225, 0.225])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
