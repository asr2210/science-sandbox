"""Experiment 013: iid with mild bias toward '2'.

Symmetry test. p = (0.2333, 0.2333, 0.30, 0.2333).
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.2333333, 0.2333333, 0.30, 0.2333334])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
