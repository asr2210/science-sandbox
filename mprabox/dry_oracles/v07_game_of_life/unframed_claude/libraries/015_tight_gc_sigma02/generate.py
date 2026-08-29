"""Per-seq GC count drawn from N(100, σ=2.0): TIGHTER than random uniform's binomial.

Random uniform 200bp has per-seq GC count ~ Binomial(200, 0.5), std=7.07.
Exp 012 (σ=0 per base) gave catastrophic 0.024.
Exp 001 (binomial, GC count std=7.07) gave 0.398.

This experiment sits between: GC count std = 2.0 (well below binomial 7.07).
A vs T and C vs G internal balance still binomial — only the GC TOTAL is constrained.

Predictions:
- T5 strict: if per-seq variance is the lever, TIGHTER than binomial should help up to a point.
- T3 strict: random uniform's binomial spread is the sweet spot; tighter hurts.
- If 015 > 0.398: tighter helps → next try σ=1.0
- If 015 ≈ 0.398: flat plateau, random uniform is at the optimum
- If 015 < 0.398: somewhere between 012's 0.024 and 001's 0.398; smooth drop

GC count target per seq: N(100, 2.0), clipped to [80, 120]. Then for each seq,
randomly select that many positions to be G or C (50/50), rest A or T (50/50).
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
GC_MEAN = 100
GC_STD = 2.0  # well below binomial std=7.07

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Per-seq GC count, integer
gc_counts = np.round(rng.normal(GC_MEAN, GC_STD, size=N)).astype(int)
gc_counts = np.clip(gc_counts, 80, 120)

seqs = []
for i in range(N):
    n_gc = int(gc_counts[i])
    n_at = L - n_gc
    # Choose which positions are GC vs AT
    pos = rng.permutation(L)
    gc_pos = pos[:n_gc]
    at_pos = pos[n_gc:]
    # Build sequence array
    arr = np.empty(L, dtype=int)
    # GC positions: randomly G(2) or C(1)
    arr[gc_pos] = rng.choice([1, 2], size=n_gc)
    # AT positions: randomly A(0) or T(3)
    arr[at_pos] = rng.choice([0, 3], size=n_at)
    seqs.append(''.join(bases[arr].tolist()))

import statistics
gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Per-seq GC: min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} "
      f"max={max(gcs):.3f} std={statistics.stdev(gcs):.4f}")
print(f"(target std = {GC_STD/L:.4f}, binomial std = {np.sqrt(0.5*0.5/L):.4f})")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
