"""001_random_uniform: 50,000 uniformly-random strings, length 200, alphabet {0,1,2,3}.

Baseline. Establishes the score for an unstructured library.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
ALPHABET = "0123"

rng = np.random.default_rng(seed=0)
idx = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
chars = np.array(list(ALPHABET))
seqs = chars[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
