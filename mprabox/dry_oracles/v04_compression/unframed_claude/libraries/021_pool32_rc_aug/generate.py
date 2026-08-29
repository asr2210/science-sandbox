"""Experiment 021: 32-pool with reverse-complement augmentation.

TFs bind both strands so half the time insert RC of the motif. This adds
strand diversity without changing pool composition. Seed=53 (best seed
from previous lottery).
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 53

MOTIFS = [
    "TGAGTCA", "TGACGTCA", "GGGCGG", "GGGGCGGGG", "GGGAATTTCC",
    "GGGACTTTCC", "GATAAG", "AGATAAG", "CCAAT", "ATTGCGCAAT",
    "TATAAA", "TATATAAA", "CACGTG", "CAGCTG", "TGTTTAC",
    "TGTTTGC", "AGGTCA", "TGACCT", "TGAAACA", "ATGCAAAT",
    "TAATCC", "CCCTC", "GCCNNNGGC", "AAACGAAACT", "TTCCNNGGAA",
    "CACCC", "CCGCCC", "TGTGGT", "TAACGG", "GCCCC",
    "CCWWWWWGG", "GTCAC",
]

COMP = {"A": "T", "T": "A", "C": "G", "G": "C",
        "N": "N", "W": "W", "S": "S", "R": "Y", "Y": "R",
        "M": "K", "K": "M", "B": "V", "V": "B", "D": "H", "H": "D"}


def rc(s):
    return "".join(COMP[c] for c in s[::-1])


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
strand = rng.integers(0, 2, size=N_SEQ)
for i in range(N_SEQ):
    motif = expand_iupac(MOTIFS[m_choice[i]], rng)
    if strand[i]:
        motif = rc(motif)
    motif_arr = np.array(list(motif))
    mlen = len(motif)
    pos = rng.integers(0, LEN - mlen + 1)
    mat[i, pos:pos + mlen] = motif_arr

with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join("".join(row) for row in mat) + "\n")
print(f"Wrote {N_SEQ} seqs; 32-pool + RC augmentation, seed={SEED}")
