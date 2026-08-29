"""Experiment 028: Uniform random seed=19.

Random seed scan to find slightly better seed (lottery).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 19

rng = np.random.default_rng(SEED)
chars = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in chars:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} uniform random sequences (seed=19) to {out_path}")
