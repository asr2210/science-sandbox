"""Experiment 1: Uniform random DNA baseline.

Generate 50,000 sequences, 200bp each, uniformly random over {A,C,G,T}.
This is the zero-prior baseline against which all future experiments will be compared.
"""

import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=1)
N, L = 50000, 200
alphabet = np.array(list("ACGT"))

# Uniform sampling
arr = rng.integers(0, 4, size=(N, L), dtype=np.int8)
seqs = ["".join(alphabet[row]) for row in arr]

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(seqs) + "\n")

print(f"Wrote {N} sequences of length {L} to {out_path}")
