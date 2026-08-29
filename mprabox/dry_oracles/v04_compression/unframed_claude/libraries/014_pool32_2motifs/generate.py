"""Experiment 014: 32-motif pool, 2 motifs per seq at non-overlapping random
positions.

Tests if doubling motif content (while keeping per-motif library frequency
low at ~6%) helps further.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
N_MOTIFS_PER_SEQ = 2
SEED = 54

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
    iupac = {
        "N": "ACGT", "W": "AT", "S": "CG", "R": "AG", "Y": "CT",
        "M": "AC", "K": "GT", "B": "CGT", "D": "AGT", "H": "ACT", "V": "ACG",
    }
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

for i in range(N_SEQ):
    used = []
    placed = 0
    attempts = 0
    while placed < N_MOTIFS_PER_SEQ and attempts < 40:
        attempts += 1
        motif = expand_iupac(MOTIFS[rng.integers(0, len(MOTIFS))], rng)
        motif_arr = np.array(list(motif))
        mlen = len(motif)
        pos = rng.integers(0, LEN - mlen + 1)
        end = pos + mlen
        if any(end <= s or pos >= e for s, e in used):
            mat[i, pos:end] = motif_arr
            used.append((pos, end))
            placed += 1
        elif not used:
            mat[i, pos:end] = motif_arr
            used.append((pos, end))
            placed += 1

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs; 32-motif pool {N_MOTIFS_PER_SEQ}/seq random pos")
