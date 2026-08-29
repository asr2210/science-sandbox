#!/usr/bin/env python3
"""UKBB-only Gosai subset (random 50K from 338K)."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    iproj = h.index("data_project")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq:
            continue
        if parts[iproj] != "UKBB":
            continue
        s = parts[iseq].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"UKBB-only valid sequences: {len(seqs)}")

rng = np.random.default_rng(SEED)
idx = rng.choice(len(seqs), size=N, replace=False)
chosen = [seqs[i] for i in idx]

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} UKBB-only sequences to {out}")
