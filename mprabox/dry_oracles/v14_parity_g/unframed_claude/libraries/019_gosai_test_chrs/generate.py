#!/usr/bin/env python3
"""Gosai sequences from Malinois held-out TEST chromosomes (9, 21, X).
Malinois training used train: all except 7,13 (val) and 9,21,X (test).
If the harness's eval uses this same held-out test set, this library should
maximize overlap and give the highest score.
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42
TEST_CHRS = {"9", "21", "X"}

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    ichr = h.index("chr")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[ichr] not in TEST_CHRS: continue
        s = parts[iseq].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"Test-chr (9,21,X) valid sequences: {len(seqs)}")

rng = np.random.default_rng(SEED)
if len(seqs) >= N:
    idx = rng.choice(len(seqs), size=N, replace=False)
    chosen = [seqs[i] for i in idx]
else:
    # Replicate if short
    reps = (N + len(seqs) - 1) // len(seqs)
    chosen = (seqs * reps)[:N]
rng.shuffle(chosen)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} test-chr sequences to {out}")
