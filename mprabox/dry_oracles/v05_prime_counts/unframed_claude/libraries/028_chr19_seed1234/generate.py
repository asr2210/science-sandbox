#!/usr/bin/env python3
"""chr19 plain random windows — SEED=1234."""
import os, numpy as np
N_SEQ, LEN, SEED = 50_000, 200, 1234
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
rng = np.random.default_rng(SEED)
seqs = []
while len(seqs) < N_SEQ:
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= valid:
        seqs.append(s)
with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 plain (seed={SEED})")
