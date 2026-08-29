"""001_random_uniform: 50,000 random DNA sequences, 200bp, uniform base frequencies."""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = bases[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out}")
