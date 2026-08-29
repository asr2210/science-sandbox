"""Experiment 006: Random TF motifs sprinkled at random positions.

Each of 50K random uniform 200bp seqs gets exactly ONE motif inserted
at a uniformly-random position. The motif identity is chosen uniformly
from a small pool of canonical TF binding sites.

Tests whether sequence-content "motif signal" helps when per-position
marginal nucleotide frequencies stay uniform (because motifs are at
varying positions and identities, the column-wise distribution remains
~uniform).

Predictions:
- T3 (uniform-i.i.d. is preferred): score still drops, because motifs
  inject structure that's locally non-uniform within each seq.
- Motif-help-with-variance: score rises above 0.331.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 46

MOTIFS = [
    "TGAGTCA",   # AP-1
    "GGGCGG",    # SP1 (GC-box)
    "GGGACTTTCC",# NF-kB (10bp)
    "GATAAG",    # GATA
    "CAATCT",    # CCAAT-like
    "TATAAA",    # TATA box (7bp)
    "CACGTG",    # E-box / MYC
    "TTGCGCAA",  # HNF-like-ish (placeholder)
]
MOTIF_ARRS = [np.array(list(m)) for m in MOTIFS]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]

m_choice = rng.integers(0, len(MOTIFS), size=N_SEQ)
for i in range(N_SEQ):
    motif = MOTIF_ARRS[m_choice[i]]
    max_pos = LEN - len(motif)
    pos = rng.integers(0, max_pos + 1)
    mat[i, pos:pos + len(motif)] = motif

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs x {LEN}bp; 1 random motif at random pos per seq")
