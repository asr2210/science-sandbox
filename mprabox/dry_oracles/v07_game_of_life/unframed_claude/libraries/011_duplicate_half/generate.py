"""25,000 unique random-uniform sequences, each duplicated to make 50,000.

Tests whether library *uniqueness* matters. If r drops vs the 50k-unique
baseline, the eval is sensitive to distinct-sequence count. If r is
unchanged, then between-sequence diversity isn't the lever — only the
marginal sequence-level statistics.
"""
import os
import numpy as np

N_UNIQUE = 25000
DUP = 2
L = 200
SEED = 42

assert N_UNIQUE * DUP == 50000

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])
arr = rng.integers(0, 4, size=(N_UNIQUE, L))
seqs = [''.join(bases[row].tolist()) for row in arr]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    for _ in range(DUP):
        for s in seqs:
            f.write(s + '\n')

# Verify
with open(out_path) as f:
    lines = f.read().splitlines()
print(f"Wrote {len(lines)} lines; unique: {len(set(lines))}")
assert len(lines) == 50000
assert len(set(lines)) == N_UNIQUE
