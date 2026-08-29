"""014 recipe (per-seq GC N(0.5, 0.075)) replicated with SEED=1.

014 scored 0.3989, slightly above random uniform 0.3981. Difference is
within the noise floor (0.0008 from 001 vs 009). This experiment validates
whether 014's elevation is reproducible or just seed noise.

If 020 ≈ 0.398-0.399, 014's bump is consistent → submit 014-style as final.
If 020 < 0.398, 014's bump was noise → default to random uniform.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 1  # different from 014's seed=42
MEAN_GC = 0.5
STD_GC = 0.075

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

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
emp = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Per-seq GC: mean={statistics.mean(emp):.3f} std={statistics.stdev(emp):.3f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
