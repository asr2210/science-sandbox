#!/usr/bin/env python3
"""50K random 200bp windows from human chr19 (hg38).
chr19 is the most gene-dense human chromosome — test if gene density
gives a bigger advantage than chr22 (gene-poor)."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 8
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
print(f"chr19 length: {len(genome)}")

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

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 windows to {OUT}")
