"""Reproducibility test: same as 001 but different seed.
Need to know if 0.4203 is noisy or reproducible."""
import numpy as np

N, L = 50000, 200
rng = np.random.default_rng(42)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = alphabet[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} random uniform sequences, seed 42")
