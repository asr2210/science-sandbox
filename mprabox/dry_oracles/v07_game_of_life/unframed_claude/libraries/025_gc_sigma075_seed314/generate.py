"""014 recipe (per-seq GC N(0.5, 0.075)) with seed=314. Continue max-of-N seed search."""
import os
import numpy as np

N = 50000
L = 200
SEED = 314
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
