"""Experiment 022: 32-pool with per-instance PWM-like noise.

For each motif instance, mutate each base with p=0.15 to a random base.
This adds per-instance variation (every motif instance is slightly
different) while keeping motif identity intact. Seed=53.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 53
MUT_P = 0.15

MOTIFS = [
    "TGAGTCA", "TGACGTCA", "GGGCGG", "GGGGCGGGG", "GGGAATTTCC",
    "GGGACTTTCC", "GATAAG", "AGATAAG", "CCAAT", "ATTGCGCAAT",
    "TATAAA", "TATATAAA", "CACGTG", "CAGCTG", "TGTTTAC",
    "TGTTTGC", "AGGTCA", "TGACCT", "TGAAACA", "ATGCAAAT",
    "TAATCC", "CCCTC", "GCCNNNGGC", "AAACGAAACT", "TTCCNNGGAA",
    "CACCC", "CCGCCC", "TGTGGT", "TAACGG", "GCCCC",
    "CCWWWWWGG", "GTCAC",
]


def expand_iupac(motif, rng):
    iupac = {"N": "ACGT", "W": "AT", "S": "CG", "R": "AG", "Y": "CT",
             "M": "AC", "K": "GT", "B": "CGT", "D": "AGT", "H": "ACT", "V": "ACG"}
    out = []
    for c in motif:
        if c in "ACGT":
            out.append(c)
        elif c in iupac:
            out.append(rng.choice(list(iupac[c])))
        else:
            out.append("A")
    return "".join(out)


rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]
m_choice = rng.integers(0, len(MOTIFS), size=N_SEQ)
for i in range(N_SEQ):
    motif = expand_iupac(MOTIFS[m_choice[i]], rng)
    mlen = len(motif)
    motif_arr = np.array(list(motif))
    # apply per-base mutations
    mask = rng.random(mlen) < MUT_P
    if mask.any():
        motif_arr[mask] = bases[rng.integers(0, 4, size=mask.sum())]
    pos = rng.integers(0, LEN - mlen + 1)
    mat[i, pos:pos + mlen] = motif_arr

with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join("".join(row) for row in mat) + "\n")
print(f"Wrote {N_SEQ} seqs; 32-pool + per-base p={MUT_P} mutation, seed={SEED}")
