"""Experiment 011: 32-motif pool, 1 motif per seq at random position.

Tests whether larger motif diversity (each motif in ~1500 seqs instead of
~6250) gives a cleaner result than exp 006.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 51

# 32 well-known TF binding motifs of varying lengths (6-10bp).
MOTIFS = [
    "TGAGTCA",     # AP-1
    "TGACGTCA",    # CREB
    "GGGCGG",      # SP1
    "GGGGCGGGG",   # SP1 long
    "GGGAATTTCC",  # NFkB
    "GGGACTTTCC",  # NFkB variant
    "GATAAG",      # GATA
    "AGATAAG",     # GATA2
    "CCAAT",       # CCAAT
    "ATTGCGCAAT",  # CEBP
    "TATAAA",      # TATA
    "TATATAAA",    # TATA long
    "CACGTG",      # Ebox
    "CAGCTG",      # Ebox variant
    "TGTTTAC",     # FOXA
    "TGTTTGC",     # FOX
    "AGGTCA",      # nuclear receptor half
    "TGACCT",      # nuclear receptor rev
    "TGAAACA",     # OCT
    "ATGCAAAT",    # POU/Oct
    "TAATCC",      # HOX
    "CCCTC",       # CTCF partial
    "GCCNNNGGC",   # CTCF-like (literal N's act as ACGT? we'll resolve below)
    "AAACGAAACT",  # IRF
    "TTCCNNGGAA",  # STAT
    "CACCC",       # KLF
    "CCGCCC",      # KLF/Sp variant
    "TGTGGT",      # RUNX
    "TAACGG",      # MYB
    "GCCCC",       # ZBTB
    "CCWWWWWGG",   # serum response (we resolve W to A/T)
    "GTCAC",       # PAX
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
            out.append("N")  # fallback
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
print(f"Wrote {N_SEQ} seqs; pool of {len(MOTIFS)} motifs, 1 per seq at random pos")
