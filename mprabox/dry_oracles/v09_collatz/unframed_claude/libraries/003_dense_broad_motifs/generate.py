"""Experiment 003: dense, broad motif panel.

Test two things at once:
  - higher motif density (12 vs 6)
  - broader panel including K562 (GATA1, KLF1, TAL1, MYB, RUNX1, PU.1)
    and neuronal (NeuroD, ASCL1 E-box, REST repressor avoided)
    and HepG2 (HNF4, HNF1, CEBP, FOXA1)
"""
import numpy as np

rng = np.random.default_rng(3)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))

MOTIFS = [
    # universal activators
    "TGAGTCA",      # AP-1
    "TGACGTCA",     # CRE
    "GGGGCGGGG",    # SP1
    "ACAGGAAGT",    # ETS/ELK
    "CCAATCG",      # CCAAT/NFY
    "TTGCGCAA",     # NRF1
    # K562 (erythroid)
    "AGATAAGA",     # GATA1
    "CACCC",        # KLF1
    "CAGGTG",       # TAL1 E-box
    "TGTGGTT",      # RUNX1
    "GAGGAAGT",     # PU.1/SPI1
    "TGCTGAGTCAT",  # NFE2 (MARE)
    # HepG2 (hepatic)
    "CAAAGGTCA",    # HNF4
    "GTTAATCATTAAC",# HNF1
    "TTGCGCAAT",    # CEBPA
    "TGTTTGC",      # FOXA1
    # neuronal (SK-N-SH)
    "CAGCTG",       # NeuroD/ASCL1 (E-box)
    "CCATATGG",     # ZIC
]

MOTIFS_PER_SEQ = 12

with open("libraries/003_dense_broad_motifs/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = list(BASES[rng.integers(0, 4, size=L)])
        chosen = rng.choice(len(MOTIFS), size=MOTIFS_PER_SEQ, replace=True)
        used = []
        for mi in chosen:
            m = MOTIFS[mi]
            ml = len(m)
            for _try in range(20):
                pos = int(rng.integers(0, L - ml + 1))
                if all(pos + ml <= s or pos >= e for s, e in used):
                    used.append((pos, pos + ml))
                    for j, ch in enumerate(m):
                        seq[pos + j] = ch
                    break
        f.write("".join(seq) + "\n")

print(f"wrote {N} sequences with {MOTIFS_PER_SEQ} motifs each from {len(MOTIFS)}-panel")
