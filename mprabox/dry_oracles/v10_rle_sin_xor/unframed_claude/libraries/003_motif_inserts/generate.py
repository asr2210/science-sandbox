"""Experiment 003: random background + 1-3 strong TF motifs inserted per sequence.

Pool covers K562 (GATA1, KLF1, TAL1), HepG2 (HNF4A, CEBPA, FOXA1), SKNSH
(NEUROD1/E-box, PHOX2B, ASCL1), plus general (SP1, AP1).
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

# Strong consensus motifs from JASPAR-like sources
MOTIFS = [
    # K562
    "AGATAAG",      # GATA1
    "CACCCAA",      # KLF1
    "CAGATGT",      # TAL1
    # HepG2
    "TGAACTTTG",    # HNF4A
    "ATTGCGCAAT",   # CEBPA
    "TGTTTACAT",    # FOXA1
    # SKNSH
    "CAGCTG",       # NEUROD1 / E-box
    "TAATCC",       # PHOX2B
    "CAGCTGT",      # ASCL1
    # general
    "GGGGCGGGGC",   # SP1
    "TGACTCA",      # AP1
    "GCCACGTG",     # MYC E-box
]

rng = np.random.default_rng(3)

# Step 1: random background
idx = rng.integers(0, 4, size=(N, L))
seqs = [list(ALPHABET[row]) for row in idx]

# Step 2: insert 2 motifs per sequence (random pick, random non-overlapping positions)
for i in range(N):
    n_inserts = rng.integers(2, 4)  # 2 or 3
    chosen = rng.choice(len(MOTIFS), size=n_inserts, replace=False)
    used = []  # (start, end)
    for mi in chosen:
        m = MOTIFS[mi]
        ml = len(m)
        # try a few times to find a non-overlapping slot
        for _ in range(8):
            start = int(rng.integers(0, L - ml + 1))
            if all(start + ml <= s or start >= e for s, e in used):
                seqs[i][start:start + ml] = list(m)
                used.append((start, start + ml))
                break

seqs_str = ["".join(s) for s in seqs]
assert all(len(s) == L for s in seqs_str)
with open(OUT, "w") as f:
    f.write("\n".join(seqs_str) + "\n")
print(f"wrote {len(seqs_str)} sequences to {OUT}")
