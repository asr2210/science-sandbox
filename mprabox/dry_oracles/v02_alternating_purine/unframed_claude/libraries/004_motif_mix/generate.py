"""Insert known TF motifs for K562/HepG2/SKNSH into random backbones.

Per sequence: pick 1-3 motifs from a curated list, insert at random
positions in a 200bp uniformly-random backbone. Vary motif count to give
the trained model an activity gradient.
"""
import os, random

random.seed(4)
N_SEQS, LENGTH = 50000, 200

# Curated TF motifs (consensus / strong)
# K562 (erythroid)
K562_MOTIFS = [
    "AGATAAG",        # GATA1
    "TGATAAG",        # GATA1
    "CACCCCACCC",     # KLF1
    "TGCTGAGTCA",     # NFE2
    "CAGCTG",         # TAL1 (E-box)
    "CAGGTG",         # TAL1
    "TGACTCA",        # AP-1
    "TGAGTCA",        # AP-1
]
# HepG2 (hepatic)
HEPG2_MOTIFS = [
    "AGGTCAAAGGTCA",  # HNF4A
    "GTTAATCATTAAC",  # HNF1
    "TGTTTGC",        # FOXA1
    "TGTTTAC",        # FOXA2
    "ATTGCGCAAT",     # CEBP
    "GGGCGGGG",       # SP1
]
# SKNSH (neuroblastoma / neuronal)
SKNSH_MOTIFS = [
    "CAGCTG",         # ASCL1 (E-box)
    "CACGTG",         # MYCN (E-box)
    "CATTTG",         # E-box variant
    "GGGAATTAA",      # PHOX2
    "AGCCAATC",       # NFI
    "TGACGTCA",       # CREB
]
ALL_MOTIFS = K562_MOTIFS + HEPG2_MOTIFS + SKNSH_MOTIFS

ALPHABET = "ACGT"

def rand_bg(n):
    return "".join(random.choices(ALPHABET, k=n))

def insert_motifs(seq, motifs):
    s = list(seq)
    for m in motifs:
        pos = random.randint(0, LENGTH - len(m))
        for i, c in enumerate(m):
            s[pos + i] = c
    return "".join(s)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N_SEQS):
        bg = rand_bg(LENGTH)
        n_motifs = random.choice([0, 1, 1, 2, 2, 3, 3, 4])  # graded
        if n_motifs == 0:
            seq = bg
        else:
            chosen = random.choices(ALL_MOTIFS, k=n_motifs)
            seq = insert_motifs(bg, chosen)
        assert len(seq) == LENGTH
        f.write(seq + "\n")
print(f"Wrote {N_SEQS} sequences (TF motif insertion)")
