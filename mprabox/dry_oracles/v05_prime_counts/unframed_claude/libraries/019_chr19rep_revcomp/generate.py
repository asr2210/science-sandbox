#!/usr/bin/env python3
"""chr19 repeat-only + reverse-complement augmentation.

25K chr19 repeat-only windows + their 25K rev-comp = 50K.
Tests if strand-axis variety boosts r without changing composition.
"""
import os
import numpy as np

N_HALF = 25_000
LEN = 200
SEED = 19
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
fwd = []
attempts = 0
while len(fwd) < N_HALF and attempts < N_HALF * 1000:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= lower_acgt:
        fwd.append(s.upper())

# Rev-comp
TAB = str.maketrans("ACGT", "TGCA")
def revcomp(s):
    return s.translate(TAB)[::-1]
rev = [revcomp(s) for s in fwd]

all_seqs = fwd + rev
rng.shuffle(all_seqs)
with open(OUT, "w") as f:
    for s in all_seqs:
        f.write(s + "\n")
print(f"Wrote {len(all_seqs)} chr19 repeat + revcomp sequences")
