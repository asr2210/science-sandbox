#!/usr/bin/env python3
"""chr19 with per-sequence gradient mutation rate (0% to 50%).

Creates wide across-library variance in "naturalness" while
backbone stays chr19. Both scoring axes should track the
mutation-rate gradient if they're sensitive to naturalness.
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 21
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
bases = np.array(list("ACGT"))

seqs = []
attempts = 0
while len(seqs) < N_SEQ and attempts < N_SEQ * 100:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if not set(s) <= valid:
        continue
    arr = np.array(list(s))
    # mutation rate linearly across library: 0..0.5
    mut_rate = (len(seqs) / N_SEQ) * 0.5
    mask = rng.random(LEN) < mut_rate
    n_mut = int(mask.sum())
    if n_mut:
        arr[mask] = bases[rng.integers(0, 4, size=n_mut)]
    seqs.append("".join(arr.tolist()))

# Shuffle so the gradient isn't in line order (matters for some metrics?)
rng.shuffle(seqs)
with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 with per-seq mut gradient (0-50%)")
