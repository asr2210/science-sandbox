#!/usr/bin/env python3
"""chr19 random 200bp windows filtered to 40-50% GC.
Tests if isolating the "sweet spot" composition within real DNA
amplifies the chr19 advantage."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 11
GC_MIN, GC_MAX = 0.40, 0.50
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip().upper())
genome = "".join(chunks)

valid_chars = set("ACGT")
rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
max_attempts = N_SEQ * 200
while len(seqs) < N_SEQ and attempts < max_attempts:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) > valid_chars:  # contains N
        continue
    gc = (s.count("G") + s.count("C")) / LEN
    if GC_MIN <= gc <= GC_MAX:
        seqs.append(s)

print(f"got {len(seqs)} windows in {attempts} attempts")
with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
