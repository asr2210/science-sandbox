#!/usr/bin/env python3
"""Zero-diversity diagnostic.

50K identical copies of one synthetic 200bp "kitchen-sink" enhancer
packed with strong canonical activator motifs. Distinguishes:
  - Per-sequence mean metric (score ~ that one seq's score)
  - Library-level metric requiring diversity (score crashes)
"""
import os

LEN = 200
N_SEQ = 50_000
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Build by repeating motif blocks until len 200
blocks = [
    "TATAAA",      # TATA
    "GGGCGG",      # SP1
    "CCAAT",       # NFY
    "CACGTG",      # E-box
    "TGACGTCA",    # CRE
    "TGAGTCA",     # AP-1
    "AGATAAG",     # GATA
    "GGAAGT",      # ETS
    "ATGCAAAT",    # OCT
    "CAGCTG",      # NeuroD/bHLH
]
seq = ""
i = 0
spacer = "AC"  # short non-motif spacer
while len(seq) < LEN:
    seq += blocks[i % len(blocks)] + spacer
    i += 1
seq = seq[:LEN]
assert len(seq) == LEN
assert set(seq) <= set("ACGT"), f"bad chars: {set(seq)}"

with open(OUT, "w") as f:
    for _ in range(N_SEQ):
        f.write(seq + "\n")

print(f"Wrote {N_SEQ} identical copies of:\n{seq}")
