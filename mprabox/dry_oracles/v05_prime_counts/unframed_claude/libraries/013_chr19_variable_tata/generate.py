#!/usr/bin/env python3
"""chr19 backbone with variable TATA box density (0-10 per seq).

Goal: create across-library variation in a single recognizable motif
so both correlation axes see varying signal."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 13
MOTIF = "TATAAA"
MAX_N = 10
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

while len(seqs) < N_SEQ:
    start = int(rng.integers(0, len(genome) - LEN))
    s = list(genome[start:start + LEN])
    if not set(s) <= valid_chars:
        continue
    n_motifs = int(rng.integers(0, MAX_N + 1))
    used = []
    placed = 0
    attempts = 0
    while placed < n_motifs and attempts < 100:
        attempts += 1
        pos = int(rng.integers(0, LEN - len(MOTIF) + 1))
        if any(pos < p + len(MOTIF) and p < pos + len(MOTIF) for p in used):
            continue
        for i, c in enumerate(MOTIF):
            s[pos + i] = c
        used.append(pos)
        placed += 1
    seqs.append("".join(s))

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19+variable-TATA sequences (0-{MAX_N} per seq)")
