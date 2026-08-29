#!/usr/bin/env python3
"""50K random 200bp windows from human chr22 (hg38).
Strips N-containing windows. Decisive test of whether REAL natural
DNA is in-distribution for the oracle."""

import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 6
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr22.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

# Read chr22 as a single uppercase sequence
chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip().upper())
genome = "".join(chunks)
print(f"chr22 length: {len(genome)}")

# Find spans without N
valid_chars = set("ACGT")
rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
max_attempts = N_SEQ * 50
while len(seqs) < N_SEQ and attempts < max_attempts:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= valid_chars:
        seqs.append(s)

if len(seqs) < N_SEQ:
    raise RuntimeError(f"only got {len(seqs)} valid windows in {attempts} tries")

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} real chr22 windows to {OUT}")
