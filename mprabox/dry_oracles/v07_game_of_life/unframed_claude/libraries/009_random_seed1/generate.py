"""Random uniform baseline with seed=1 instead of 42.

Measures the library-resampling noise floor for the score. If 009 and 001
score within ~0.001 of each other, the small differences I've measured
across libraries (e.g., 0.005 between random and chr22 tiles) are real
library effects, not seed noise.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 1

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in seqs:
        f.write(''.join(row.tolist()) + '\n')
print(f"Wrote {N} sequences (seed {SEED}) to {out_path}")
