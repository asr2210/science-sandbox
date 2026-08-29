"""Exp 023: pure uniform random with seed=99.
Third data point for noise floor distribution.
"""
import numpy as np, os

N = 50_000
L = 200
SEED = 99
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr].astype("<U1")

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} random seed={SEED}")
