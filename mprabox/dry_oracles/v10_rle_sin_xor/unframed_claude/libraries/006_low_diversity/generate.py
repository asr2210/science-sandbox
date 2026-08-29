"""Experiment 006: low-diversity library.

All 50,000 sequences are derived from a single random 50%-GC scaffold by
mutating each position independently with probability 0.05. This tests
whether *reducing* prediction variance further pushes K562 r above 0.99.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(6)
scaffold = rng.integers(0, 4, size=L)

idx = np.tile(scaffold, (N, 1)).copy()
mut_mask = rng.random(size=(N, L)) < 0.05
# new bases: random 0..3 with replacement (will sometimes equal original; that's fine)
new_bases = rng.integers(0, 4, size=(N, L))
idx[mut_mask] = new_bases[mut_mask]

seqs = ["".join(ALPHABET[row]) for row in idx]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
