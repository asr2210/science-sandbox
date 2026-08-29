"""Experiment 011: iid with mild composition bias toward char '0'.

Each character sampled iid with p = (0.30, 0.2333, 0.2333, 0.2333).
Mild bias - 5% more '0' than uniform. Tests if any per-char preference exists.

Predictions:
- > 0.42: '0' is preferred
- ≈ 0.42: symmetric
- < 0.42: uniform composition is strictly best
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.30, 0.2333333, 0.2333333, 0.2333334])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, composition target: {p}")
