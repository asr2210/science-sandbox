"""Experiment 015: 32-motif pool, 1 motif/seq, seed 100. Replicate."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

N_SEQ, LEN, SEED = 50000, 200, 300

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
    return "".join(c if c in "ACGT" else rng.choice(list(iupac.get(c, "A"))) for c in motif)


rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
mat = bases[rng.integers(0, 4, size=(N_SEQ, LEN))]
m_choice = rng.integers(0, len(MOTIFS), size=N_SEQ)
for i in range(N_SEQ):
    motif = expand_iupac(MOTIFS[m_choice[i]], rng)
    motif_arr = np.array(list(motif))
    mlen = len(motif)
    pos = rng.integers(0, LEN - mlen + 1)
    mat[i, pos:pos + mlen] = motif_arr

with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join("".join(row) for row in mat) + "\n")
print(f"Wrote {N_SEQ} seqs; 32-pool seed={SEED}")
