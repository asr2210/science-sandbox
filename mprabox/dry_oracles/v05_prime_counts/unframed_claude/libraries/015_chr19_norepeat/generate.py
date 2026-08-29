#!/usr/bin/env python3
"""chr19 windows REPEAT-FILTERED via soft-mask.

chr19.fa is soft-masked: lowercase = repeats (LINE/SINE/Alu/etc).
Keep only windows where all 200bp are UPPERCASE ACGT (non-repeat).

Tests whether removing repeat sequences (which are ~60% of chr19)
boosts eval_01 above the 0.050 ceiling of all-chr19 windows.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 15
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

# Keep case (do NOT .upper())
chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip())
genome = "".join(chunks)

upper_acgt = set("ACGT")
rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
max_attempts = N_SEQ * 1000
while len(seqs) < N_SEQ and attempts < max_attempts:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    # all chars must be uppercase ACGT (non-repeat, non-N)
    if set(s) <= upper_acgt:
        seqs.append(s)

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 non-repeat windows ({attempts} attempts)")
