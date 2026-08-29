"""Experiment 013: Real chr22 backbone + insert strong known TF motifs.
Each sequence gets 3-5 randomly placed canonical motifs from a curated set
covering K562, HepG2, SK-N-SH-relevant TFs and broad activators.
Tests whether ENGINEERED motif density boosts the score over plain real DNA.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
SRC = os.path.join(os.path.dirname(__file__), "..", "005_real_human_chr22", "sequences_0.txt")
L = 200

# Strong canonical TF binding motifs (consensus, fixed)
MOTIFS = [
    "AGATAA",        # GATA1 (K562 erythroid)
    "AGATAAGR".replace("R", "A"),  # GATA palindrome
    "CAGATG",        # TAL1/SCL E-box
    "CACGTG",        # MYC/USF E-box
    "CCAATC",        # NFY
    "GGGCGG",        # SP1
    "GGGCGGGG",      # SP1 stronger
    "TGASTCA".replace("S", "G"),   # AP-1
    "TGACTCA",       # AP-1 alt
    "GGAATG",        # ETS family
    "CCGGAA",        # ETS
    "TTGCGCAAT",     # CEBP (HepG2)
    "TGAACT",        # FOXA1/HNF (HepG2)
    "TGTTTGY".replace("Y", "C"),   # HNF1A
    "CAACTGTG",      # ZEB
    "TAATCC",        # HOX
    "GCCNNNGGC".replace("N", "A"), # KLF
    "TTATCT",        # SOX
    "GGGAAATTCCC",   # NF-kB
    "CCACGTGG",      # E-box variant
    "TGTGGT",        # YY1
    "TATAAA",        # TATA box
    "TATATAA",       # TATA variant
    "GCGCCGCG",      # CpG enriched
    "AAACAGCTGTTT",  # E-box palindrome
]

with open(SRC) as f:
    src_seqs = [ln.strip() for ln in f if ln.strip()]
print(f"Loaded {len(src_seqs)} chr22 sequences")
rng = np.random.default_rng(80)

out = []
for s in src_seqs:
    arr = bytearray(s, "ascii")
    n_motifs = rng.integers(3, 6)  # 3-5 motifs per sequence
    for _ in range(n_motifs):
        m = MOTIFS[rng.integers(0, len(MOTIFS))]
        if len(m) >= L:
            continue
        pos = rng.integers(0, L - len(m))
        arr[pos:pos+len(m)] = m.encode()
    out.append(arr.decode())
print(f"Built {len(out)} motif-stuffed sequences")
# Sanity check lengths
assert all(len(o) == L for o in out)
with open(OUT, "w") as f:
    f.write("\n".join(out) + "\n")
print("Done.")
