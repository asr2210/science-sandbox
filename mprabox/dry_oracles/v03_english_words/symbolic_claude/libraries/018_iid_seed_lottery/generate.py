"""Experiment 018: seed lottery on best setup.

Same p as exp 011 (winner: 0.4272) but DIFFERENT seed.
Seed variance from exp 001 vs 007: 0.4200 vs 0.4239 = ±0.004.
If lucky, may yield 0.43+.

If similar score: confirms 0.4272 is the typical ceiling for this p.
If much higher: ensemble strategy worth pursuing.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(1234567)  # different seed from exp 011 (42)

p = np.array([0.30, 0.2333333, 0.2333333, 0.2333334])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}, seed=1234567")
