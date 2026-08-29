#!/usr/bin/env python3
"""chr19 STRIDED non-overlapping 200bp windows.

Tile chr19 with non-overlapping windows. Skip any window with N
or repeats? Use upper-converted chr19. Sample with explicit stride.
Tests if systematic coverage beats random sampling at the ceiling.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

chunks = []
with open(FA) as fh:
    for line in fh:
        if not line.startswith(">"):
            chunks.append(line.strip().upper())
genome = "".join(chunks)
valid = set("ACGT")
# Stride windows
seqs = []
# Need 50K windows × 200bp = 10Mb; chr19 has ~58Mb; pick stride.
# Use exact 200bp non-overlap walk, skipping N-containing.
for start in range(0, len(genome) - LEN, LEN):
    s = genome[start:start + LEN]
    if set(s) <= valid:
        seqs.append(s)
    if len(seqs) >= N_SEQ:
        break
# Pad if needed with random sampling
rng = np.random.default_rng(30)
while len(seqs) < N_SEQ:
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= valid:
        seqs.append(s)

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 strided non-overlapping windows")
