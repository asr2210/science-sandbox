"""Experiment 012: 64-motif pool. Tests if larger pool continues helping.

Doubles pool size: each motif appears in ~780 seqs (1.6% library frequency).
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 52

# 64 motifs: 32 from exp 011 plus 32 more (variants and additional TFs).
MOTIFS = [
    # Original 32
    "TGAGTCA", "TGACGTCA", "GGGCGG", "GGGGCGGGG", "GGGAATTTCC",
    "GGGACTTTCC", "GATAAG", "AGATAAG", "CCAAT", "ATTGCGCAAT",
    "TATAAA", "TATATAAA", "CACGTG", "CAGCTG", "TGTTTAC",
    "TGTTTGC", "AGGTCA", "TGACCT", "TGAAACA", "ATGCAAAT",
    "TAATCC", "CCCTC", "GCCNNNGGC", "AAACGAAACT", "TTCCNNGGAA",
    "CACCC", "CCGCCC", "TGTGGT", "TAACGG", "GCCCC",
    "CCWWWWWGG", "GTCAC",
    # 32 more
    "TGTGGTTT",     # RUNX long
    "TGAGTCAT",     # AP-1 ext
    "AGGAAG",       # ETS
    "GGAANNGGAA",   # ETS dimer
    "TAATTA",       # HOX/POU
    "AATTGCAT",     # OCT-1
    "CTTTCA",       # FOX
    "GGGGGCGGGG",   # SP1 long2
    "GTGGGCGG",     # SP-like
    "TTTCCNNNGAAA", # STAT-like
    "TGACCTNN",     # NR
    "AGRACA",       # nuclear half
    "TGTTNN",       # FOX-like
    "CAGGTG",       # E-box variant
    "CATTTG",       # E-box variant
    "TGTTGAC",      # CBFA2T3
    "AGCAGCTG",     # E-box
    "CCATATATGG",   # MEF2
    "CATGTG",       # E-box
    "TGAGGAA",      # ETS-AP1
    "TGACTCA",      # AP-1 variant
    "RGGNCCY",      # SRF
    "CCWWWWWWGG",   # SRF long
    "AGGTCANNAGGTCA",# DR2
    "AGGTCANNNNAGGTCA",# DR5
    "TGACTAA",      # bZIP-like
    "GAAANNGAAA",   # IRF dimer
    "CCAATCA",      # NF-Y
    "TTGCATAT",     # POU
    "ACGTGT",       # MYB / b-ZIP
    "CCAGGTGG",     # SMAD bind
    "AGCTGCT",      # SMAD-like
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

m_choice = rng.integers(0, len(MOTIFS), size=N_SEQ)
for i in range(N_SEQ):
    motif = expand_iupac(MOTIFS[m_choice[i]], rng)
    motif_arr = np.array(list(motif))
    mlen = len(motif)
    pos = rng.integers(0, LEN - mlen + 1)
    mat[i, pos:pos + mlen] = motif_arr

seqs = ["".join(row) for row in mat]
with open(os.path.join(os.path.dirname(__file__), "sequences_0.txt"), "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N_SEQ} seqs; pool of {len(MOTIFS)} motifs")
