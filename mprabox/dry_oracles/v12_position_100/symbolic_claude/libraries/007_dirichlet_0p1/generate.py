"""Exp 007: Dirichlet(0.1) — more extreme per-seq compositions."""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(13)
weights = rng.dirichlet([0.1, 0.1, 0.1, 0.1], size=N)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    idx = rng.choice(4, size=L, p=weights[i])
    lines.append("".join(chars[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} dir(0.1) seqs")
