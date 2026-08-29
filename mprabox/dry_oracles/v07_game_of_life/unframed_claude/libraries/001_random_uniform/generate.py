"""Random uniform baseline. 50,000 sequences of 200bp, each base i.i.d. uniform from ACGT."""
import numpy as np
import os

N = 50000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])
arr = rng.integers(0, 4, size=(N, L))
seqs = bases[arr]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for row in seqs:
        f.write(''.join(row.tolist()) + '\n')

print(f"Wrote {N} sequences of length {L} to {out_path}")
