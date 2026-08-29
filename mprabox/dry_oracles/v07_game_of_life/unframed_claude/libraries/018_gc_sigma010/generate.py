"""Per-seq GC from N(0.5, 0.10) — push plateau upper edge.

Plateau confirmed flat from σ=0.010 (015) to σ=0.082 (014). 005 (σ≈0.23) dropped to 0.365.
Where exactly does the cliff start? 018 tests σ=0.10, between 014 and 005.

Predicted:
- If plateau extends to 0.10: r ≈ 0.398.
- If cliff starts at 0.10: r between 0.380 and 0.398.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
MEAN_GC = 0.5
STD_GC = 0.10

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

gcs = rng.normal(MEAN_GC, STD_GC, size=N)
gcs = np.clip(gcs, 0.15, 0.85)

seqs = []
for gc in gcs:
    pA = pT = (1 - gc) / 2
    pC = pG = gc / 2
    probs = np.array([pA, pC, pG, pT])
    arr = rng.choice(4, size=L, p=probs)
    seqs.append(''.join(bases[arr].tolist()))

import statistics
emp = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Per-seq GC: min={min(emp):.3f} mean={statistics.mean(emp):.3f} "
      f"max={max(emp):.3f} std={statistics.stdev(emp):.3f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
