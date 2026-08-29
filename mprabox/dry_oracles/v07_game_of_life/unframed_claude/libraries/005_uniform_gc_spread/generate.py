"""Per-sequence GC content drawn from U(0.1, 0.9).

Library has 50,000 sequences; each one's GC fraction sampled uniformly from
0.1..0.9 (so the library spans the full feasible GC range smoothly).
Mean GC ≈ 0.5 with extreme within-library variance.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Sample per-sequence GC content
gcs = rng.uniform(0.1, 0.9, size=N)
seqs = []
for gc in gcs:
    pA = pT = (1 - gc) / 2
    pC = pG = gc / 2
    probs = np.array([pA, pC, pG, pT])
    arr = rng.choice(4, size=L, p=probs)
    seqs.append(''.join(bases[arr].tolist()))

import statistics
emp_gc = [sum(c in 'GC' for c in s) / L for s in seqs]
print(f"Empirical GC: min={min(emp_gc):.3f} mean={statistics.mean(emp_gc):.3f} "
      f"max={max(emp_gc):.3f} std={statistics.stdev(emp_gc):.3f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
