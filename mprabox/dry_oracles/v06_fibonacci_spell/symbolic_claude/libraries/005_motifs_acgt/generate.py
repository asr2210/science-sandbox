"""Experiment 005: Universal regulatory motifs, mapping 0123 -> ACGT.

For each of 50K random length-200 sequences, insert K ~ Uniform(0, 12)
copies of randomly chosen well-known TF binding motifs at random
positions. The variation in motif count and identity should create
wide variance in predicted activities IF the eval model uses 0->A,
1->C, 2->G, 3->T (standard ML convention).

Universal motifs used (active across many cell types):
  TATA  : TATAAA   (core promoter)
  Ebox  : CAGCTG   (Myc family)
  GCbox : GGGCGG   (SP1)
  CAAT  : CCAATC
  AP1   : TGASTCA  (use TGAGTCA)
  CRE   : TGACGTCA
  NFkB  : GGGACTTTCC
  GATA  : AGATAA   (GATA family - strong in K562)
  HNF4  : AGGTCA   (strong in HepG2)
"""
import os
import numpy as np

N_SEQS = 50_000
LEN = 200
SEED = 23

# 0=A, 1=C, 2=G, 3=T
ENC = {"A": "0", "C": "1", "G": "2", "T": "3"}
def encode(s):
    return "".join(ENC[c] for c in s)

MOTIFS = [encode(m) for m in (
    "TATAAA", "CAGCTG", "GGGCGG", "CCAATC", "TGAGTCA", "TGACGTCA",
    "GGGACTTTCC", "AGATAA", "AGGTCA",
)]

rng = np.random.default_rng(SEED)

# Start from uniform random base
seqs = rng.integers(0, 4, size=(N_SEQS, LEN), dtype=np.uint8)
chars = np.array(list("0123"))

# Convert to list of mutable bytearrays for in-place edits
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N_SEQS):
        seq = list(chars[seqs[i]])
        n_insert = int(rng.integers(0, 13))  # 0..12 inclusive
        for _ in range(n_insert):
            m = MOTIFS[rng.integers(0, len(MOTIFS))]
            pos = int(rng.integers(0, LEN - len(m) + 1))
            for k, ch in enumerate(m):
                seq[pos + k] = ch
        f.write("".join(seq) + "\n")
print(f"Wrote {N_SEQS} sequences to {out_path}")
