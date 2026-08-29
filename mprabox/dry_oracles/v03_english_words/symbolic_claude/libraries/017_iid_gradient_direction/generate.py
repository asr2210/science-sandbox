"""Experiment 017: gradient-direction tuning.

Combine the partial signals from exp 011-014. Mild '0' boost + mild '3' reduce,
with '1','2' near baseline. Tests whether asymmetric tuning beats single-char bias.

p = (0.30, 0.245, 0.235, 0.22). Total deviation from uniform: 0.05+0.005+0.015+0.03 = 0.10.

Predictions:
- > 0.4272: gradient direction helps beyond exp 011
- ≈ 0.4272: '0' boost dominates; '3' reduction neutralized
- < 0.4272: any added bias on '3' hurts more than '0' gain
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

p = np.array([0.30, 0.245, 0.235, 0.22])
arr = rng.choice(4, size=(N, L), p=p).astype(np.uint8)

with open("sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, p={p}")
