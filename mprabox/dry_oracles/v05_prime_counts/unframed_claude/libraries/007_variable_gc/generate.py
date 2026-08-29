#!/usr/bin/env python3
"""Variable GC across library: each sequence has its own GC drawn from
Uniform[0.2, 0.8], then bases sampled iid at that GC.

Tests whether across-library GC variance is the lever (mimicking
chr22's varied composition without the genuine biology)."""
import numpy as np
import os

N_SEQ = 50_000
LEN = 200
SEED = 7
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
# Each sequence: its own GC
gcs = rng.uniform(0.2, 0.8, size=N_SEQ)

with open(OUT, "w") as f:
    for gc in gcs:
        # base probs: G,C share gc/2; A,T share (1-gc)/2
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=LEN, p=p)
        f.write("".join(bases[idx].tolist()) + "\n")

print(f"Wrote {N_SEQ} variable-GC sequences (per-seq GC ~ U(0.2,0.8))")
