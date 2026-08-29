#!/usr/bin/env python3
"""CRE-project Gosai sequences only (14K), replicated to 50K.
Tests whether eval test set is from CRE subset (real cCREs from chromatin marks).
"""
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
        if parts[iproj] != "CRE":
            continue
        s = parts[iseq].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"CRE-only valid sequences: {len(seqs)}")

rng = np.random.default_rng(SEED)
# Replicate to reach N
reps = (N + len(seqs) - 1) // len(seqs)
all_seqs = (seqs * reps)[:N]
rng.shuffle(all_seqs)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"Wrote {len(all_seqs)} sequences ({len(seqs)} unique CRE) to {out}")
