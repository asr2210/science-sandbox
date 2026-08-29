"""Baseline: 50,000 uniformly random 200bp sequences."""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(42)
N, L = 50_000, 200
ALPH = np.array(list("ACGT"))

idx = rng.integers(0, 4, size=(N, L))
seqs = ALPH[idx]

out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    for row in seqs:
        f.write("".join(row) + "\n")

print(f"wrote {N} sequences to {out}")
