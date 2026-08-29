#!/usr/bin/env python3
"""Gosai sequences from TRAIN chrs only (exclude 7, 9, 13, 21, X).
Test if any eval uses Malinois training set as ground truth (which would
be unusual but possible if eval is a downstream model trained on held-out)."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42
EXCLUDE = {"7", "9", "13", "21", "X"}

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    ichr = h.index("chr")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[ichr] in EXCLUDE: continue
        s = parts[iseq].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"Train-chr (not 7,9,13,21,X) valid: {len(seqs)}")

rng = np.random.default_rng(SEED)
idx = rng.choice(len(seqs), size=N, replace=False)
chosen = [seqs[i] for i in idx]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} train-chr sequences to {out}")
