"""Per-sequence GC drawn from N(0.5, 0.075), clipped to [0.20, 0.80].

This gives roughly 2× the per-seq GC variance of random uniform (which has
binomial GC std ~0.035). Tests T5: if more per-seq variance helps r,
this should beat random uniform. If random uniform is already optimal,
this should be ≤ 0.398. If too wide, it should drop further.

Mean GC = 0.5; per-seq GC std = 0.075.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
MEAN_GC = 0.5
STD_GC = 0.075

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Sample per-seq GC, clip to plausible range
gcs = rng.normal(MEAN_GC, STD_GC, size=N)
gcs = np.clip(gcs, 0.20, 0.80)

seqs = []
for gc in gcs:
    pA = pT = (1 - gc) / 2
    pC = pG = gc / 2
    probs = np.array([pA, pC, pG, pT])
    arr = rng.choice(4, size=L, p=probs)
    seqs.append(''.join(bases[arr].tolist()))

import statistics
empgc = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Empirical GC: min={min(empgc):.3f} mean={statistics.mean(empgc):.3f} "
      f"max={max(empgc):.3f} std={statistics.stdev(empgc):.3f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
