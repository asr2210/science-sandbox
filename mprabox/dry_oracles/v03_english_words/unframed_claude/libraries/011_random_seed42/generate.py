"""Exp 011: Pure uniform random with seed=42. Tests noise floor.
Compares directly to Exp 001 (seed=0).
"""
import numpy as np, os

N = 50_000
L = 200
rng = np.random.default_rng(42)
bases = np.array(list("ACGT"))
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")
print(f"Wrote {N} sequences (seed=42)")
