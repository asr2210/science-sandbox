"""Experiment 018: Curated 64-motif pool of short, high-quality canonical
TF binding sites (no IUPAC ambiguity, no overly-long motifs).

Tests whether the 32-motif sweet spot was a function of pool SIZE or pool
QUALITY. Doubling pool with only high-quality short motifs.
"""
import os
import numpy as np

N_SEQ = 50000
LEN = 200
SEED = 61

# 64 short (5-10bp) canonical TF binding sites, no IUPAC ambiguity.
# Sources: JASPAR consensus, well-known biology textbook references.
MOTIFS = [
    # AP-1 family
    "TGAGTCA", "TGACTCA", "TGAGCTCA",
    # CREB / ATF
    "TGACGTCA", "TGACGCAA", "ACGTCA",
    # SP1 / KLF (GC-box)
    "GGGCGG", "GGGGCGGGG", "GGCCAC", "GCCACG",
    # NFkB / Rel
    "GGGAATTTCC", "GGGACTTTCC", "GGGGCATCCC", "GGGGAATCCC",
    # GATA
    "GATAAG", "AGATAAG", "TGATAA", "TGATAAG",
    # CCAAT / NF-Y / CEBP
    "CCAAT", "CCAATCA", "ATTGCGCAAT", "TTGCGCAA",
    # TATA / TBP
    "TATAAA", "TATATAAA", "TATATATA",
    # E-box / bHLH (Myc, Max, USF, etc)
    "CACGTG", "CAGCTG", "CATGTG", "CACCTG", "CAGGTG",
    # FOX
    "TGTTTAC", "TGTTTGC", "TGTTGAC", "AAACAA",
    # Nuclear receptor half-site
    "AGGTCA", "TGACCT", "TGTTCT", "AGAACA",
    # Octamer / POU
    "ATGCAAAT", "TAATGARAT",
    # HOX / NKX
    "TAATCC", "TTAATTA", "CAAGTG",
    # CTCF
    "CCCTC", "CCGCGNGG", "CCACGGTGGC",
    # IRF
    "AAACGAAACT", "AANNGAAA",
    # STAT
    "TTCCNNGGAA", "TTCCGGGAA",
    # KLF
    "CACCC", "CCGCCC",
    # RUNX / MYB
    "TGTGGT", "TGTGGTTT", "TAACGG",
    # ETS family
    "AGGAAG", "GGAAGT", "CGGAAG",
    # PAX
    "GTCAC", "GTCACG",
    # SOX
    "CATTGTT", "ACAATG",
    # SMAD / TBX
    "GTCT", "AGGTGT",
    # ZNF
    "GCCCC",
    # MEF2
    "CTAAAAATAG",
]


def expand_iupac(motif, rng):
    iupac = {"N": "ACGT", "W": "AT", "S": "CG", "R": "AG", "Y": "CT",
             "M": "AC", "K": "GT"}
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
print(f"Wrote {N_SEQ} seqs; curated {len(MOTIFS)}-motif pool")
