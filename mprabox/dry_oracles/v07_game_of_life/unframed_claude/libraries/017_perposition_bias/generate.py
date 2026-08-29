"""Per-position base bias with library-averaged uniform marginals.

At each position i, one base is favored with prob 0.35 and the other three
share 0.2167 each (sums to 1). Which base is favored rotates every position:
i%4==0 → A, i%4==1 → C, i%4==2 → G, i%4==3 → T.

Library marginal (average over positions): each base = 0.25 exactly.
Per-seq A count: 50 positions at p=0.35 + 150 positions at p=0.2167.
  Expected = 50*0.35 + 150*0.2167 = 50.0 (same as binomial mean).
  Variance = 50*0.35*0.65 + 150*0.2167*0.7833 = 36.9. Std=6.07 (≈binomial 6.12).

Library marginal stats: identical to random uniform.
Per-seq stats: nearly identical to random uniform.
DIFFERENCE: per-POSITION distribution. Position 0 has 35% A, position 1 has 35% C, etc.

Tests whether the eval is sensitive to per-position structure even when library
marginals and per-seq stats match. If the eval prediction depends purely on
per-seq composition stats, 017 ≈ 0.398. If it captures positional context,
017 should differ.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
FAVORED = 0.35
OTHER = (1 - FAVORED) / 3  # = 0.2167

assert abs(FAVORED + 3 * OTHER - 1.0) < 1e-9
assert abs((FAVORED + 3 * OTHER) / 4 - 0.25) < 1e-9  # library marginal = 0.25 per base

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Build per-position probability matrix: shape (L, 4)
probs = np.full((L, 4), OTHER)
for i in range(L):
    fav = i % 4
    probs[i, fav] = FAVORED

# Verify column averages = 0.25
assert np.allclose(probs.mean(axis=0), 0.25)

# Sample sequences
arr = np.zeros((N, L), dtype=int)
for i in range(L):
    arr[:, i] = rng.choice(4, size=N, p=probs[i])

import statistics
gcs = [sum(c in [1, 2] for c in row) / L for row in arr[:2000]]
acounts = [int((row == 0).sum()) for row in arr[:2000]]
print(f"Per-seq GC: mean={statistics.mean(gcs):.3f} std={statistics.stdev(gcs):.4f}")
print(f"Per-seq A count: mean={statistics.mean(acounts):.2f} std={statistics.stdev(acounts):.3f}")
print(f"(binomial reference: GC std=0.035, A std=6.12)")

# Library marginal check
library_mean_a = float((arr == 0).mean())
print(f"Library A frequency: {library_mean_a:.4f} (target 0.25)")

seqs = [''.join(bases[row].tolist()) for row in arr]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
