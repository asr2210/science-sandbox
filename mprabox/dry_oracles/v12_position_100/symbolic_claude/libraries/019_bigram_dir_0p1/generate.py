"""Exp 019: Bigram-Dir with α=0.1.

Same as exp 010 (best so far, 0.0784) but with sparser per-seq bigram dist.
Tests if alpha sweep on bigram-Dir can push past 0.0784.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(91)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    bw = rng.dirichlet([0.1] * 16).reshape(4, 4)
    row_sums = bw.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    P = bw / row_sums
    pi = bw.sum(axis=1)
    pi = pi / pi.sum() if pi.sum() > 0 else np.ones(4) / 4

    seq = np.empty(L, dtype=np.int8)
    seq[0] = rng.choice(4, p=pi)
    for t in range(1, L):
        seq[t] = rng.choice(4, p=P[seq[t-1]])
    lines.append("".join(chars[seq]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} bigram-Dir(0.1) seqs")
