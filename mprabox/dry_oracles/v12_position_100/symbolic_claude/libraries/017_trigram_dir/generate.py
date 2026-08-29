"""Exp 017: trigram-Dir.

Per seq, sample 64 trigram weights from Dir(α=0.3, over 64).
Generate seq using 2nd-order Markov chain conditional on last 2 chars.

Tests if higher-order k-mer structure adds signal beyond bigram.
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(67)
chars = np.array(list("0123"))

lines = []
for i in range(N):
    w = rng.dirichlet([0.3] * 64).reshape(4, 4, 4)  # [a, b, c] joint
    # marginal P(a, b) by summing over c
    pab = w.sum(axis=2)
    # transition P(c | a, b) = w[a, b, c] / pab[a, b]
    pab_safe = np.where(pab > 0, pab, 1.0)
    P = w / pab_safe[:, :, None]
    # marginal over a (for first char)
    pa = pab.sum(axis=1)
    pa = pa / pa.sum() if pa.sum() > 0 else np.ones(4) / 4

    seq = np.empty(L, dtype=np.int8)
    seq[0] = rng.choice(4, p=pa)
    # P(b | a) = pab[a, b] / pa[a]
    pba_safe = np.where(pa > 0, pa, 1.0)
    Pba = pab / pba_safe[:, None]
    Pba_row = Pba[seq[0]] / max(Pba[seq[0]].sum(), 1e-12)
    seq[1] = rng.choice(4, p=Pba_row)
    for t in range(2, L):
        row = P[seq[t-2], seq[t-1]]
        s = row.sum()
        if s > 0:
            seq[t] = rng.choice(4, p=row / s)
        else:
            seq[t] = rng.integers(0, 4)
    lines.append("".join(chars[seq]))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} trigram-Dir seqs")
