"""Experiment 024: 8-motif pool (extreme small pool).

Tests lower boundary: does even smaller pool concentrate signal more?
Picked 8 most-canonical, most-distinct motifs (different families).
Seed=53.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 53

MOTIFS = [
    "TGAGTCA",    # AP-1
    "TGACGTCA",   # CREB
    "GGGCGG",     # SP1
    "GGGAATTTCC", # NFkB
    "GATAAG",     # GATA
    "TATAAA",     # TATA
    "CACGTG",     # E-box (Myc)
    "AGGTCA",     # NR
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
print(f"Wrote {N_SEQ} seqs; 8-motif pool seed={SEED}")
