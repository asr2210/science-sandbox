#!/usr/bin/env python3
"""chr19 windows ENRICHED for ENCODE TFBS clusters.

For each TFBS peak (chr19), take the center as a 200bp window.
These should be biologically active regulatory regions.
50K windows sampled from ENCODE TFBS clusters on chr19.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 22
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
BED = os.path.join(ROOT, "data", "chr19_tfbs.bed")
OUT = os.path.join(HERE, "sequences_0.txt")

chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip().upper())
genome = "".join(chunks)

# Parse BED, get peak centers
centers = []
with open(BED) as fh:
    for line in fh:
        parts = line.rstrip().split("\t")
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        c = (start + end) // 2
        centers.append(c)
centers = np.array(centers)
print(f"chr19 TFBS peaks: {len(centers)}")

valid = set("ACGT")
rng = np.random.default_rng(SEED)
seqs = []
# Random sample with replacement
idx = rng.integers(0, len(centers), size=N_SEQ * 2)
for i in idx:
    if len(seqs) >= N_SEQ:
        break
    c = int(centers[i])
    start = c - LEN // 2
    if start < 0 or start + LEN > len(genome):
        continue
    s = genome[start:start + LEN]
    if set(s) <= valid:
        seqs.append(s)

# Fallback: keep sampling if not enough
while len(seqs) < N_SEQ:
    i = int(rng.integers(0, len(centers)))
    c = int(centers[i])
    start = c - LEN // 2
    if start < 0 or start + LEN > len(genome):
        continue
    s = genome[start:start + LEN]
    if set(s) <= valid:
        seqs.append(s)

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 TFBS-centered sequences")
