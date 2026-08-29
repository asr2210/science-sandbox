"""Each per-base count drawn from N(50, σ_target≈1.3), independent across bases.

Test target: per-seq per-base count std ≈ 1.3 (much tighter than random uniform's
binomial std = 6.12, but well above 012's zero).

Method:
  For each seq:
    1. Draw raw (a', c', g', t') ~ N(50, 1.5) independently
    2. Subtract mean so they sum to 200 in expectation
    3. Round and adjust residual to make exact integer sum = 200
    4. Randomly arrange those base counts into a length-200 sequence

Predicted per-base count std after centering: ~1.5 * sqrt(3/4) ≈ 1.30

Bracket check:
  012 (per-base std=0):     r=0.024  ← catastrophe
  001 (per-base std=6.12):  r=0.398  ← plateau center
  This 016 (per-base std≈1.3): r=?

If T6 plateau extends to tight per-base variance: r ≈ 0.398.
If smooth decline between 012 and 001: r ≈ 0.25 (interpolated).
If there's a soft floor at σ≈1: r between 0.15-0.30.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
RAW_STD = 1.5

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Sample raw counts, center them so each seq sums exactly to L=200 integer.
raw = rng.normal(0.0, RAW_STD, size=(N, 4))
raw -= raw.mean(axis=1, keepdims=True)  # zero-mean per seq
fractional = 50.0 + raw  # each seq, four floats summing to 200.0

# Convert to integers summing exactly to 200 per seq.
def to_int_counts(floats):
    """Round to ints, then fix sum to exactly 200 by adjusting the largest residuals."""
    ints = np.floor(floats).astype(int)
    residual = 200 - ints.sum()
    if residual > 0:
        # Add 1 to the components with largest fractional parts
        frac = floats - ints
        order = np.argsort(-frac)
        for k in range(residual):
            ints[order[k % 4]] += 1
    elif residual < 0:
        frac = floats - ints
        order = np.argsort(frac)  # smallest first
        for k in range(-residual):
            ints[order[k % 4]] -= 1
    return np.clip(ints, 0, L)  # safety

all_counts = np.array([to_int_counts(fractional[i]) for i in range(N)])
assert (all_counts.sum(axis=1) == L).all(), "counts must sum to L"

# Quick stat
import statistics
per_base_a = all_counts[:, 0]
per_base_t = all_counts[:, 3]
print(f"Per-seq A count: mean={per_base_a.mean():.2f} std={per_base_a.std():.3f}")
print(f"Per-seq T count: mean={per_base_t.mean():.2f} std={per_base_t.std():.3f}")
print(f"(binomial reference std = {np.sqrt(L * 0.25 * 0.75):.3f}, 012 std = 0)")

seqs = []
for i in range(N):
    c = all_counts[i]
    # Build sequence: c[0] A's, c[1] C's, c[2] G's, c[3] T's, then permute
    arr = np.concatenate([np.full(c[k], k, dtype=int) for k in range(4)])
    arr = arr[rng.permutation(L)]
    seqs.append(''.join(bases[arr].tolist()))

gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
print(f"Per-seq GC: min={min(gcs):.3f} mean={statistics.mean(gcs):.3f} "
      f"max={max(gcs):.3f} std={statistics.stdev(gcs):.4f}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
