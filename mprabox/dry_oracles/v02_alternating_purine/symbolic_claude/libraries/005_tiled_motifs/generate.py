"""005_tiled_motifs: per-string repeated motif.

For each of 50,000 strings:
  - Pick a motif length k ~ Uniform{2,3,4,5,6,7,8,9,10}
  - Pick a random motif of length k from {0,1,2,3}^k
  - Tile to length 200
This creates a library with high periodic/repetitive structure variation.
Tests whether scoring rewards periodicity / k-mer richness.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
chars = "0123"

rng = np.random.default_rng(seed=5)
ks = rng.integers(2, 11, size=N)
out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for i in range(N):
        k = int(ks[i])
        motif_idx = rng.integers(0, 4, size=k)
        motif = "".join(chars[j] for j in motif_idx)
        # tile and trim
        reps = (L + k - 1) // k
        s = (motif * reps)[:L]
        assert len(s) == L
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
