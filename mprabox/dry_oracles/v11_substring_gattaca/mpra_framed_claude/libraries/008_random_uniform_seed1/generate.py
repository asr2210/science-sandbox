"""Experiment 008: noise floor check. Exact replica of exp 001 with seed=1."""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 1

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = alphabet[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences of length {L} to {out}")
