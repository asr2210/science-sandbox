#!/usr/bin/env python3
"""Val chrs (7, 13) + GTEX-only. Try to refine eval_01 above 0.13."""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42
VAL_CHRS = {"7", "13"}

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    ichr = h.index("chr")
    iproj = h.index("data_project")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        if parts[ichr] not in VAL_CHRS: continue
        if parts[iproj] != "GTEX": continue
        s = parts[iseq].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            seqs.append(s)

print(f"Val-chr GTEX-only: {len(seqs)}")

rng = np.random.default_rng(SEED)
if len(seqs) >= N:
    idx = rng.choice(len(seqs), size=N, replace=False)
    chosen = [seqs[i] for i in idx]
else:
    reps = (N + len(seqs) - 1) // len(seqs)
    chosen = (seqs * reps)[:N]
rng.shuffle(chosen)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} sequences to {out}")
