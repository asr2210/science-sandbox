"""Every sequence has exactly 50% GC (100 G/C and 100 A/T, random positions).

Pinpoints whether *removing* the small natural GC noise around 50% (binomial
spread in random uniform) further improves r. If so, libraries should be
controlled to exactly 50% GC. If not, random uniform is already optimal-ish.
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42
HALF = L // 2  # 100

rng = np.random.default_rng(SEED)
bases_gc = np.array(['C', 'G'])
bases_at = np.array(['A', 'T'])

seqs = []
for _ in range(N):
    # Choose 100 GC positions
    gc_positions = rng.choice(L, size=HALF, replace=False)
    gc_mask = np.zeros(L, dtype=bool)
    gc_mask[gc_positions] = True
    # Fill in: pick A/T or C/G randomly within their slots
    gc_picks = rng.integers(0, 2, size=HALF)
    at_picks = rng.integers(0, 2, size=HALF)
    out = np.empty(L, dtype='<U1')
    out[gc_mask] = bases_gc[gc_picks]
    out[~gc_mask] = bases_at[at_picks]
    seqs.append(''.join(out.tolist()))

# Sanity check
gcs = [sum(c in 'GC' for c in s) / L for s in seqs]
print(f"GC distribution: unique values = {sorted(set(gcs))}")
assert all(gc == 0.5 for gc in gcs)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
