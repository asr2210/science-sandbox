"""Experiment 004: high-density motif library.

Each 200bp sequence is a concatenation of ~10 motifs separated by short
random spacers, padded with random nucleotides. Tests whether dense motif
loading lifts HepG2/SKNSH.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

MOTIFS = [
    # K562
    "AGATAAG",      # GATA1
    "CACCCAA",      # KLF1
    "CAGATGT",      # TAL1
    "GGGAGCCAA",    # NFE2
    # HepG2
    "TGAACTTTG",    # HNF4A
    "ATTGCGCAAT",   # CEBPA
    "TGTTTACAT",    # FOXA1
    "GTTAATNATTAAC",# HNF1A-like
    # SKNSH
    "CAGCTG",       # E-box / NEUROD1
    "TAATCC",       # PHOX2B
    "CACGTG",       # MYC E-box
    "TAATTA",       # homeobox
    # general
    "GGGGCGGGGC",   # SP1
    "TGACTCA",      # AP1
    "CCAATCA",      # CCAAT box
    "TATAAAA",      # TATA box
]

rng = np.random.default_rng(4)

def make_seq():
    parts = []
    used = 0
    while used < L - 12:
        if rng.random() < 0.7:  # 70% motif, 30% spacer
            m = MOTIFS[rng.integers(len(MOTIFS))]
            # random IUPAC N → random nucleotide
            m = "".join(ALPHABET[rng.integers(4)] if c == "N" else c for c in m)
        else:
            m = "".join(ALPHABET[rng.integers(4, size=rng.integers(1, 5))])
        parts.append(m)
        used += len(m)
    s = "".join(parts)
    if len(s) > L:
        s = s[:L]
    elif len(s) < L:
        pad = "".join(ALPHABET[rng.integers(4, size=L - len(s))])
        s += pad
    return s

seqs = [make_seq() for _ in range(N)]
assert all(len(s) == L for s in seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
