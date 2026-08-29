"""Exp 006: Dirichlet-extreme compositions.

Each sequence draws its own composition weights from Dirichlet(0.3,0.3,0.3,0.3).
Low concentration → highly biased per-seq compositions.
This amplifies the across-sequence compositional variance vs uniform random.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(11)
weights = rng.dirichlet([0.3, 0.3, 0.3, 0.3], size=N)  # (N, 4)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    idx = rng.choice(4, size=L, p=weights[i])
    lines.append("".join(chars[idx]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} dirichlet-extreme seqs")
