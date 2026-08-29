#!/usr/bin/env python3
"""chr19 windows with WITHIN-SEQ SHUFFLE.

Take each chr19 200bp window, shuffle its bases. Preserves
per-sequence composition exactly; destroys positional grammar.

If score = chr19 plain → composition is the lever.
If score << chr19 → positional grammar matters.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 23
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

valid = set("ACGT")
rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
while len(seqs) < N_SEQ and attempts < N_SEQ * 100:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= valid:
        arr = np.array(list(s))
        rng.shuffle(arr)
        seqs.append("".join(arr.tolist()))

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19-shuffled (composition-preserving)")
