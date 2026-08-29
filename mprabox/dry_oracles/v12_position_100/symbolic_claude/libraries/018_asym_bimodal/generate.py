"""Exp 018: ASYMMETRIC Dir with bimodal axis per sub-library.

50K = 12.5K per group. Each group has Dir(α, β, β, β) where one position has
low α (≈ bimodal: very low or very high q_k) and others moderate β.

Tests if any specific character axis dominates the signal.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
PER = N // 4

rng = np.random.default_rng(71)
chars = np.array(list("0123"))

LOW = 0.05
HIGH = 0.5

lines = []
for axis in range(4):
    alphas = [HIGH] * 4
    alphas[axis] = LOW
    weights = rng.dirichlet(alphas, size=PER)
    for i in range(PER):
        idx = rng.choice(4, size=L, p=weights[i])
        lines.append("".join(chars[idx]))

rng.shuffle(lines)
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} asymmetric Dir bimodal seqs")
