"""Exp 014: Dir(0.5) — alpha between 0.3 (best) and 1.0."""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(41)
weights = rng.dirichlet([0.5] * 4, size=N)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    idx = rng.choice(4, size=L, p=weights[i])
    lines.append("".join(chars[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} Dir(0.5) seqs")
