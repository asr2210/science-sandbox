#!/usr/bin/env python3
"""Higher-density motif packing with extended panel and graded density.

Design:
- 50K sequences split into 10 density tiers (5K each): 0, 2, 4, 6, 8, 10, 12, 14, 16, 18 motifs
- This creates a strong continuous gradient of motif content
- Goal: produce libraries where a trained predictor has lots of variance to learn
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 43

MOTIFS = [
    # K562/erythroid
    "AGATAA", "TTATCT", "CAGCTG", "CACCC", "GGGTGG",
    "TGCTGAGTCAY".replace("Y", "C"),
    # HepG2/liver
    "AGTCCAAAGTCCA", "GTTAATAATTAAC", "TGTTTAC", "TTGCGCAAT", "ATTGCGCAA",
    "TGAACAGT", "GGGCAAATGGTCA",
    # Neural
    "TTCAGCACCNCGGNGAGCAGCAC".replace("N", "A"),
    "CAGCTG",  # ASCL1
    "CTGCAG",  # ASCL1 rev
    # Ubiquitous/strong
    "GGGCGG", "GGGGCGGGGC", "CCGCCC",  # SP1
    "TATAAA", "CCAAT", "CCAATC",
    "TGACTCA", "TGACGTCA",
    "CACGTG", "CATGTG",
    "ATGCAAAT",                  # OCT
    "TTCCGGAA", "GAAACCGGAAGT",  # IRF/ETS
    "ACAGGAAGT", "AAAGAGGAAGT", "CGGAAGT",  # ETS/ELK
    "CCATCTT", "AAGATGG",        # YY1
    "CCCTC", "GAGGG",
    "CAGGTG", "CACCTG",          # E-box variants
    "GCCNNNGGC".replace("N", "A"),  # AP-2 like
    "TTTGCGCAAT", "ATTGCGCAAA",
    "GACCAG", "CTGGTC",
    "GCATGCG",
    "ATATAA",
    "TGACATCA",
]

# Filter to ACGT-only
MOTIFS = [m for m in MOTIFS if set(m) <= set("ACGT")]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

motif_arrs = [np.array(list(m)) for m in MOTIFS]
motif_lens = [len(m) for m in motif_arrs]

# Density tiers
tiers = np.repeat(np.arange(0, 19, 2), N // 10)  # 5000 each, 10 tiers
# Make exactly N
if len(tiers) < N:
    tiers = np.concatenate([tiers, np.full(N - len(tiers), tiers[-1])])
rng.shuffle(tiers)

for i in range(N):
    k = int(tiers[i])
    if k == 0:
        continue
    occupied = np.zeros(L, dtype=bool)
    chosen = rng.integers(0, len(MOTIFS), size=k)
    order = rng.permutation(k)
    for idx in order:
        m_idx = int(chosen[idx])
        mlen = motif_lens[m_idx]
        for _ in range(12):
            pos = int(rng.integers(0, L - mlen + 1))
            if not occupied[pos:pos+mlen].any():
                seqs[i, pos:pos+mlen] = motif_arrs[m_idx]
                occupied[pos:pos+mlen] = True
                break

lines = ["".join(row) for row in seqs]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} dense-motif sequences to {out}")
print(f"Motifs in panel: {len(MOTIFS)}; density tiers 0..18")
