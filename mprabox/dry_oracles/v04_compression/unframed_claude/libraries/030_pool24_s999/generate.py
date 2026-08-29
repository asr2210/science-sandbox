"""Experiment 025: 24-motif pool (between 16 and 32).

Locate the sweet spot more precisely. Seed=53.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 999

MOTIFS = [
    "TGAGTCA",    # AP-1
    "TGACGTCA",   # CREB
    "GGGCGG",     # SP1
    "GGGGCGGGG",  # SP1/KLF
    "GGGAATTTCC", # NFkB
    "GGGACTTTCC", # NFkB
    "GATAAG",     # GATA
    "AGATAAG",    # GATA
    "CCAAT",      # CCAAT
    "TATAAA",     # TATA
    "TATATAAA",   # TATA
    "CACGTG",     # E-box (Myc)
    "CAGCTG",     # E-box
    "TGTTTAC",    # FOX
    "AGGTCA",     # NR
    "TGACCT",     # NR (RC)
    "ATGCAAAT",   # OCT
    "TAATCC",     # HOX
    "CCCTC",      # CTCF
    "TGTGGT",     # RUNX
    "TAACGG",     # ETS
    "CACCC",      # KLF
    "CCGCCC",     # KLF
    "GTCAC",      # PAX
]


rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]
m_choice = rng.integers(0, len(MOTIFS), size=N_SEQ)
for i in range(N_SEQ):
    motif = MOTIFS[m_choice[i]]
    motif_arr = np.array(list(motif))
    mlen = len(motif)
    pos = rng.integers(0, LEN - mlen + 1)
    mat[i, pos:pos + mlen] = motif_arr

with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join("".join(row) for row in mat) + "\n")
print(f"Wrote {N_SEQ} seqs; 24-motif pool seed={SEED}")
