#!/usr/bin/env python3
"""Pack each random sequence with a random subset of common TF motifs.
Tests whether motif diversity unlocks score.

Approach:
- For each of 50K sequences: start with random ACGT background
- Sample N motifs (0-6) from a panel; place at random non-overlapping positions
- This creates diversity in motif content per sequence
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

# Panel of common TF motifs (consensus or near-consensus sequences)
# Covers K562 (GATA1, TAL1, KLF1), HepG2 (HNF4A, HNF1A, FOXA1, CEBPA),
# neural (REST/NRSF, ASCL1), and general (SP1, TATA, CAAT, AP1, CREB,
# MYC, USF, NRF1, YY1, NFY, ETS)
MOTIFS = [
    "AGATAA",       # GATA1
    "CAGCTG",       # E-box (TAL1, ASCL1, NEUROD1, MYOD)
    "CACCC",        # KLF1
    "TGCTGAGTCA",   # NFE2/AP-1-like
    "AGTCCAAAGTCCA",# HNF4A
    "GTTAATAATTAAC",# HNF1A palindrome
    "TGTTTAC",      # FOXA1
    "TTGCGCAAT",    # CEBP
    "GGGCGG",       # SP1
    "TATAAA",       # TATA
    "CCAAT",        # CAAT/NFYA
    "TGACTCA",      # AP1
    "TGACGTCA",     # CREB
    "CACGTG",       # MYC/USF (E-box variant)
    "GCGCATGCGC",   # NRF1
    "CCATCTT",      # YY1
    "ACAGGAAGT",    # ETS
    "AAAGAGGAAGT",  # ELK1
    "GGGCGGGGC",    # SP1 stronger
    "ATGCAAAT",     # OCT
    "TTCCGGAA",     # IRF
    "GACCACAG",     # SRF
    "CTGTGGTC",     # SRF reverse
    "CCCTC",        # CTCF-ish
    "CTCCC",        # KLF reverse
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

# Pre-decode motifs to arrays
motif_arrs = [np.array(list(m)) for m in MOTIFS]
motif_lens = [len(m) for m in motif_arrs]

n_motifs_per_seq = rng.integers(0, 7, size=N)  # 0..6 motifs

for i in range(N):
    k = int(n_motifs_per_seq[i])
    if k == 0:
        continue
    # Pick k motifs (with replacement)
    chosen = rng.integers(0, len(MOTIFS), size=k)
    # Find non-overlapping positions greedily
    occupied = np.zeros(L, dtype=bool)
    # Random order
    order = rng.permutation(k)
    for idx in order:
        m_idx = int(chosen[idx])
        mlen = motif_lens[m_idx]
        # Try a few random positions
        for _ in range(8):
            pos = int(rng.integers(0, L - mlen + 1))
            if not occupied[pos:pos+mlen].any():
                seqs[i, pos:pos+mlen] = motif_arrs[m_idx]
                occupied[pos:pos+mlen] = True
                break

lines = ["".join(row) for row in seqs]
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} sequences with random TF motif panels to {out}")
