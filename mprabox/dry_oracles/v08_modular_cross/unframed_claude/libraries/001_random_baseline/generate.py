"""Uniform random DNA baseline: 50,000 sequences of 200bp."""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
seqs = rng.choice(bases, size=(N, L))
lines = ["".join(row) for row in seqs]

out = Path(__file__).parent / "sequences_0.txt"
out.write_text("\n".join(lines) + "\n")
print(f"Wrote {N} sequences of length {L} to {out}")
