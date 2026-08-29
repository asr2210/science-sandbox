"""Experiment 001: uniformly random 200bp sequences (baseline / floor)."""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
out_path = Path(__file__).parent / "sequences_0.txt"

# Vectorized: one big random matrix, then join per row
idx = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
seqs = bases[idx]
with out_path.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
