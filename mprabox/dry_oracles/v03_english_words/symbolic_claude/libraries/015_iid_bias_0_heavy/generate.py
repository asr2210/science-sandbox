"""Experiment 015: iid with HEAVIER bias toward '0'.

Push further in the breakthrough direction from exp 011.
p = (0.40, 0.20, 0.20, 0.20). 10% more '0' than uniform.

If linear: ~0.434. If hurts (too skewed): < 0.4272.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.40, 0.20, 0.20, 0.20])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
