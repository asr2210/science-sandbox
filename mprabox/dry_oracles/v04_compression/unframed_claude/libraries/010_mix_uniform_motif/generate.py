"""Experiment 010: 50/50 mix of uniform random and motif-loaded sequences.

25,000 uniform random + 25,000 with one random motif (from 8-motif pool)
at a random position. Shuffled together.

Hypothesis: creates variance in "predicted activity space" across the
library (some seqs predicted higher activity due to motifs, others not),
which might improve Pearson r if both predictor and target track this.
"""
import os
import numpy as np

N_TOTAL = 50000
N_UNIFORM = 25000
N_MOTIF = 25000
LEN = 200
SEED = 50

MOTIFS = [
    "TGAGTCA", "GGGCGG", "GGGACTTTCC", "GATAAG",
    "CAATCT", "TATAAA", "CACGTG", "TTGCGCAA",
]
MOTIF_ARRS = [np.array(list(m)) for m in MOTIFS]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# uniform random part
uni = bases[rng.integers(0, 4, size=(N_UNIFORM, LEN))]

# motif-loaded part
mot = bases[rng.integers(0, 4, size=(N_MOTIF, LEN))]
m_idx = rng.integers(0, len(MOTIFS), size=N_MOTIF)
for i in range(N_MOTIF):
    motif = MOTIF_ARRS[m_idx[i]]
    pos = rng.integers(0, LEN - len(motif) + 1)
    mot[i, pos:pos + len(motif)] = motif

# shuffle together
mat = np.concatenate([uni, mot], axis=0)
perm = rng.permutation(N_TOTAL)
mat = mat[perm]

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_TOTAL} seqs; 50% uniform + 50% with 1 random motif")
