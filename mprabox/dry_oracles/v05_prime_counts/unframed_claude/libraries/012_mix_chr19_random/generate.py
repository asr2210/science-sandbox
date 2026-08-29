#!/usr/bin/env python3
"""Mixed library: 25K chr19 real windows + 25K uniform random.

eval_08 loves uniform random (random>>chr19 there).
Other evals slightly prefer chr19.
Mixing may raise the average."""
import os
import numpy as np

N_EACH = 25_000
LEN = 200
SEED = 12
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FA = os.path.join(ROOT, "data", "chr19.fa")
OUT = os.path.join(HERE, "sequences_0.txt")

# chr19 part
chunks = []
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            continue
        chunks.append(line.strip().upper())
genome = "".join(chunks)

valid_chars = set("ACGT")
rng = np.random.default_rng(SEED)
chr_seqs = []
attempts = 0
while len(chr_seqs) < N_EACH and attempts < N_EACH * 100:
    attempts += 1
    start = int(rng.integers(0, len(genome) - LEN))
    s = genome[start:start + LEN]
    if set(s) <= valid_chars:
        chr_seqs.append(s)

# Random uniform part
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_EACH, LEN))
rand_seqs = ["".join(row.tolist()) for row in bases[idx]]

# Mix and shuffle so they're interleaved
all_seqs = chr_seqs + rand_seqs
rng.shuffle(all_seqs)
with open(OUT, "w") as f:
    for s in all_seqs:
        f.write(s + "\n")
print(f"Wrote 25K chr19 + 25K uniform random = {len(all_seqs)} sequences")
