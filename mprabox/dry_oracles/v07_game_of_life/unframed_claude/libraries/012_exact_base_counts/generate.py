"""Each sequence contains exactly 50 of each base (A, C, G, T).

Tighter than 006 (which only fixed GC=50%): forces *every* base to appear
exactly 50 times, eliminating natural per-sequence base composition
fluctuations entirely. If the eval prefers maximally-balanced sequences,
this might give a small boost over random uniform.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42

assert L % 4 == 0
PER_BASE = L // 4

rng = np.random.default_rng(SEED)

# Each sequence: 50 A's, 50 C's, 50 G's, 50 T's, shuffled.
template = np.repeat(np.arange(4), PER_BASE)  # [0,0,...,1,1,...,2,2,...,3,3,...]
bases = np.array(['A', 'C', 'G', 'T'])

seqs = []
for _ in range(N):
    perm = rng.permutation(L)
    arr = template[perm]
    seqs.append(''.join(bases[arr].tolist()))

import statistics
counts_check = [(s.count('A'), s.count('C'), s.count('G'), s.count('T')) for s in seqs[:1000]]
print(f"All seqs have counts (A,C,G,T) = (50,50,50,50): {all(c == (50,50,50,50) for c in counts_check)}")
gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:1000]]
print(f"GC: min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} max={max(gcs):.3f}")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
