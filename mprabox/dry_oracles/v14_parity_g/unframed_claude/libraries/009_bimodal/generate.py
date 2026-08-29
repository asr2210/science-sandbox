#!/usr/bin/env python3
"""Bimodal library: half sequences have many TF motifs, half are pure random.
Tests whether strong variance in motif content drives stronger signal."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

MOTIFS = [
    "AGATAA", "TTATCT", "CAGCTG", "CACCC", "GGGTGG",
    "AGTCCAAAGTCCA", "GTTAATAATTAAC", "TGTTTAC", "TTGCGCAAT",
    "GGGCGG", "TATAAA", "CCAAT", "TGACTCA", "TGACGTCA",
    "CACGTG", "ATGCAAAT", "TTCCGGAA", "ACAGGAAGT",
    "GGGCGGGGC", "CCATCTT",
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

# First N/2 sequences get many motifs (10-15 each)
motif_arrs = [np.array(list(m)) for m in MOTIFS]
motif_lens = [len(m) for m in motif_arrs]

half = N // 2
for i in range(half):
    k = int(rng.integers(10, 16))
    occupied = np.zeros(L, dtype=bool)
    chosen = rng.integers(0, len(MOTIFS), size=k)
    order = rng.permutation(k)
    for idx in order:
        m_idx = int(chosen[idx])
        mlen = motif_lens[m_idx]
        for _ in range(15):
            pos = int(rng.integers(0, L - mlen + 1))
            if not occupied[pos:pos+mlen].any():
                seqs[i, pos:pos+mlen] = motif_arrs[m_idx]
                occupied[pos:pos+mlen] = True
                break

# Last N/2: leave random (no motifs)

# Shuffle order so high/low sequences are interleaved
perm = rng.permutation(N)
seqs = seqs[perm]

lines = ["".join(row) for row in seqs]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} bimodal sequences to {out}")
