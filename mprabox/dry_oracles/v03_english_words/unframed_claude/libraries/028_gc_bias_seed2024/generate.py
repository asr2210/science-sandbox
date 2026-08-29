"""Exp 028: random with slight GC bias.
p_A = p_T = 0.23, p_C = p_G = 0.27 (GC=54%). Seed=2024 (top-2 random seed).
Tests if model prefers slightly GC-enriched random.
"""
import numpy as np, os
N, L, SEED = 50_000, 200, 2024
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
p = np.array([0.23, 0.27, 0.27, 0.23])

arr = rng.choice(4, size=(N, L), p=p)
seqs = bases[arr].astype("<U1")
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} GC-bias (p_C=p_G=0.27)")
