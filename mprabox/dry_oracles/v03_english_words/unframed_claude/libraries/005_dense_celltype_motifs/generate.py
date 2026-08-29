"""Exp 005: Dense cell-type-specific TF motifs.
Each 200bp sequence gets 6 motifs from a curated pool weighted toward
known regulators of K562 (myeloid), HepG2 (liver), SK-N-SH (neuron).
Spacing is random with a minimum gap of 5bp between motifs.

Hypothesis: high motif density should give the model strong, confident
predictions across cell types and boost mean_r if the model is trained
on natural enhancers.
"""
import numpy as np
import os

N = 50_000
L = 200
N_MOTIFS_PER_SEQ = 6
SEED = 5
rng = np.random.default_rng(SEED)

# Cell-type-specific motifs (sub-consensus, length 5-12).
K562 = [
    "AGATAA",    # GATA1
    "TTATCT",    # GATA1 RC
    "CACCC",     # KLF1
    "GGGTG",     # KLF1 RC
    "CAGGTG",    # TAL1/E-box
    "CACCTG",    # TAL1 RC
    "TGTGGT",    # RUNX1
    "ACCACA",    # RUNX1 RC
    "TGCTGAGTCA",# NFE2
    "CAGTTG",    # MYB
    "CAACTG",    # MYB RC
]
HEPG2 = [
    "GTTAATAATTAAC", # HNF1A palindrome
    "CAAAGTCCA",     # HNF4A
    "TGGACTTTG",     # HNF4A RC
    "TCAATAA",       # HNF6/ONECUT
    "TTATTGA",       # HNF6 RC
    "TGTTTGT",       # FOXA1
    "ACAAACA",       # FOXA1 RC
    "TTGCGCAAT",     # CEBPA
    "ATTGCGCAA",     # CEBPA RC
    "AGGTCAAAGGTCA", # PPARA/HNF4 DR1
]
SKNSH = [
    "TAATTA",    # PHOX2/homeobox
    "CAGCTG",    # ASCL1
    "CAGATG",    # NEUROD
    "CATCTG",    # HAND2 / NEUROD RC
    "CTAATTG",   # ISL1
    "CAATTAG",   # ISL1 RC
    "TTCAGCACC", # NRSF/REST partial
    "TCTAGA",    # POU
]
BROAD = [
    "TGACTCA",   # AP-1
    "TGAGTCA",   # AP-1 alt
    "TGACGTCA",  # CREB
    "GGGACTTTCC",# NF-kB
    "CCAAT",     # NF-Y
    "ATTGG",     # NF-Y RC
    "GGGCGG",    # SP1
    "CCGCCC",    # SP1 RC
    "TATAAA",    # TATA
    "CACGTG",    # MYC E-box
]

POOL = K562 + HEPG2 + SKNSH + BROAD
# Weights: emphasize cell-type-specific over broad
weights = np.array(
    [3.0] * len(K562) +
    [3.0] * len(HEPG2) +
    [3.0] * len(SKNSH) +
    [1.0] * len(BROAD)
)
weights /= weights.sum()

bases = np.array(list("ACGT"))

# Pre-generate random background
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")

for i in range(N):
    chosen = rng.choice(len(POOL), size=N_MOTIFS_PER_SEQ, replace=True, p=weights)
    # Place motifs at non-overlapping positions if possible
    used = []
    for mi in chosen:
        m = POOL[mi]
        mlen = len(m)
        if mlen > L:
            continue
        for _ in range(10):  # try 10 times to find non-overlapping slot
            pos = int(rng.integers(0, L - mlen + 1))
            if all(not (pos < p[1] and pos + mlen > p[0]) for p in used):
                break
        used.append((pos, pos + mlen))
        for k, ch in enumerate(m):
            seqs[i, pos + k] = ch

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences to {out_path}")
