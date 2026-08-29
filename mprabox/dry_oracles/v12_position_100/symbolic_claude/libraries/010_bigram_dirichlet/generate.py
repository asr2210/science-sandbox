"""Exp 010: Per-seq bigram distribution sampled from Dirichlet over 16 bigrams.

Each seq draws bigram weights from Dir(0.3, over 16 bigrams). Then builds the
seq as a Markov walk: each next char is drawn given the previous, with
transition probs derived from the bigram weights.

Tests if BIGRAM compositional variance (beyond monomer) adds signal.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(23)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    # 16 bigram weights from Dir(0.3)
    bw = rng.dirichlet([0.3] * 16)  # (16,)
    bw = bw.reshape(4, 4)  # [prev, next]
    # Marginal over prev (stationary): solve for stationary dist via row sums
    # Use bw as joint, normalize per row to transition matrix
    row_sums = bw.sum(axis=1, keepdims=True)
    # Avoid div-by-zero for any row
    row_sums = np.where(row_sums == 0, 1, row_sums)
    P = bw / row_sums  # transition matrix
    # Marginal stationary: just use row sums of bw (proportional)
    pi = bw.sum(axis=1)
    pi = pi / pi.sum() if pi.sum() > 0 else np.ones(4) / 4

    seq = np.empty(L, dtype=np.int8)
    seq[0] = rng.choice(4, p=pi)
    for t in range(1, L):
        seq[t] = rng.choice(4, p=P[seq[t-1]])
    lines.append("".join(chars[seq]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} bigram-Dirichlet seqs")
