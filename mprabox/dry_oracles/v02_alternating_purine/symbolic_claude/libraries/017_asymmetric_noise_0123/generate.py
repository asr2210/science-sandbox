"""Exp 017: period-4 (0,1,2,3) with asymmetric noise.

Per position i:
- template base (i mod 4): prob 0.7
- "next" base ((i+1) mod 4): prob 0.2
- other two: prob 0.05 each
Total = 1.0; all bases present at every position (min 0.05).
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 17

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
# Per-position distribution: build a (4, 4) matrix where row i is the
# distribution at positions where template-base == i.
# But the "next base" depends on (i mod 4), so it's a single transition matrix.
# Map: t_base -> distribution over (0,1,2,3)
dist_for_tbase = np.zeros((4, 4))
for t in range(4):
    nxt = (t + 1) % 4
    dist_for_tbase[t, t] = 0.7
    dist_for_tbase[t, nxt] = 0.2
    for k in range(4):
        if k != t and k != nxt:
            dist_for_tbase[t, k] = 0.05
assert np.allclose(dist_for_tbase.sum(axis=1), 1.0)

# For each (sequence, position), sample base from dist_for_tbase[template[pos]]
# Vectorise via cumulative sum and uniform draws.
cum = dist_for_tbase.cumsum(axis=1)  # (4, 4)
pos_cum = cum[template]              # (L, 4)
u = rng.random((N, L))                # (N, L)
# tokens[i,j] = first k such that u[i,j] < pos_cum[j,k]
seqs = (u[:, :, None] >= pos_cum[None, :, :]).sum(axis=2).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

# sanity
pos0_freqs = [(seqs[:, 0] == b).mean() for b in range(4)]
pos1_freqs = [(seqs[:, 1] == b).mean() for b in range(4)]
print(f"wrote {N}; pos-0 freqs (expect 0.7/0.2/0.05/0.05) = {[round(x,3) for x in pos0_freqs]}")
print(f"           pos-1 freqs (expect 0.05/0.7/0.2/0.05) = {[round(x,3) for x in pos1_freqs]}")
print(f"unique={len(set(map(bytes, seqs)))}")
