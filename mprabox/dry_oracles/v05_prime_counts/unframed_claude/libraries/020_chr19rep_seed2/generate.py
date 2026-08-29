#!/usr/bin/env python3
"""chr19 repeat-only with DIFFERENT SEED (variance check).

Tests library-side noise. If score differs much from exp 16
(0.0518), the 0.0518 was a lucky sample. If similar, it's signal.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 2020  # different seed
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip())
genome = "".join(chunks)

lower_acgt = set("acgt")
rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
while len(seqs) < N_SEQ and attempts < N_SEQ * 1000:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= lower_acgt:
        seqs.append(s.upper())

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 repeat-only sequences (seed={SEED})")
