#!/usr/bin/env python3
"""chr19 windows REPEAT-ONLY (all lowercase soft-masked).

Test counter-hypothesis: non-repeat HURT (exp 15) — does pure
repeat HELP, or is the chr19 mix what gives 0.050?
"""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 42
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
max_attempts = N_SEQ * 1000
while len(seqs) < N_SEQ and attempts < max_attempts:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= lower_acgt:
        seqs.append(s.upper())  # uppercase for downstream scoring

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} chr19 repeat-only windows ({attempts} attempts)")
