"""Experiment 020: Peak finding — milder '0' bias.

p = (0.275, 0.2417, 0.2417, 0.2416). Halfway between uniform and exp 011.
If milder bias is better, peak is below 0.30. If worse, peak is at 0.30+.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.275, 0.2417, 0.2417, 0.2416])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
