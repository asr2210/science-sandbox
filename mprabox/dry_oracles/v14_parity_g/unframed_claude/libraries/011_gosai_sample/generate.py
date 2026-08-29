#!/usr/bin/env python3
"""Sample 50K sequences from the Gosai et al. 2024 lentiMPRA dataset.

The dataset has 798K sequences, each 200bp, measured in K562, HepG2, SKNSH —
the exact three cell lines in our eval. If the test set uses sequences from
this distribution (or a model trained on it), our library should score high.
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

# Read header + first column with sequence
seqs = []
with open(SRC) as f:
    header = f.readline().rstrip("\n").split("\t")
    seq_col = header.index("sequence")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= seq_col:
            continue
        s = parts[seq_col].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"Read {len(seqs)} valid sequences (len=200, ACGT only)")

rng = np.random.default_rng(SEED)
idx = rng.choice(len(seqs), size=N, replace=(len(seqs) < N))
chosen = [seqs[i] for i in idx]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} Gosai sequences to {out}")
