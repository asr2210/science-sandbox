#!/usr/bin/env python3
"""Motif-cocktail library.

Each 200bp sequence = uniform random background with ~10 strong regulatory
motifs inserted at random non-overlapping positions. Mix of cell-type
agnostic activators + canonical motifs from K562/HepG2/SK-N-SH literature.
"""
import numpy as np
import os

N_SEQ = 50_000
LEN = 200
SEED = 2
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
MOTIFS_PER_SEQ = 10

# Each entry: canonical consensus, forward strand
MOTIFS = [
    # General / core promoter
    "GGGCGG",      # SP1
    "CCAAT",       # NFY / CCAAT-box
    "TATAAA",      # TATA box
    "TCAGTT",      # INR-like
    "CACGTG",      # E-box (USF/MYC)
    "TGACGTCA",    # CRE (CREB)
    "TGAGTCA",     # AP-1
    "GGGRNNYYCC".replace("R","G").replace("Y","C").replace("N","A"),  # NFKB-ish
    "GCCACGTGGC",  # extended E-box
    "ATGCAAAT",    # OCT (POU)
    "GGAAGT",      # ETS
    # Cell-type specific
    "AGATAAG",     # GATA (K562 lineage)
    "CACCTG",      # E-box (TAL1/E-protein, K562)
    "GTTAATCATTAAC",   # HNF1 (HepG2)
    "TGAACTTTG",   # HNF4 (HepG2)
    "CAGCTG",      # bHLH / NeuroD (SK-N-SH)
    "CATATG",      # NeuroD2 / MyoD E-box
    "CCGCCATCTT",  # Sp1-like extended
]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

def make_seq():
    seq = list(bases[rng.integers(0, 4, size=LEN)])
    # pick non-overlapping positions
    chosen = []
    attempts = 0
    while len(chosen) < MOTIFS_PER_SEQ and attempts < 200:
        attempts += 1
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        pos = int(rng.integers(0, LEN - len(m) + 1))
        # check non-overlap
        ok = True
        for (p, l) in chosen:
            if not (pos + len(m) <= p or pos >= p + l):
                ok = False
                break
        if not ok:
            continue
        # 50% reverse complement
        if rng.random() < 0.5:
            comp = {"A":"T","T":"A","C":"G","G":"C"}
            m = "".join(comp[c] for c in m[::-1])
        for i, c in enumerate(m):
            seq[pos + i] = c
        chosen.append((pos, len(m)))
    return "".join(seq)

with open(OUT, "w") as f:
    for _ in range(N_SEQ):
        f.write(make_seq() + "\n")

print(f"Wrote {N_SEQ} sequences with motif cocktail to {OUT}")
