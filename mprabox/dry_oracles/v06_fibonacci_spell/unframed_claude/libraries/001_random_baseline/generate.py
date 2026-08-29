"""Experiment 001: Random uniform baseline.

50,000 sequences of 200bp, each base sampled uniformly from {A,C,G,T}.
This calibrates the scoring floor — what does pure entropy get us?
"""
import numpy as np

N = 50_000
L = 200
SEED = 0

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = bases[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} sequences of length {L}")
