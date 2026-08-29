"""Exp 025: period-4 (0,1,2,3) with PREV-in-cycle biased asymmetric noise.

Per position i (template = i mod 4):
- template base: 0.7
- previous-in-cycle ((i-1) mod 4): 0.2
- other two: 0.05 each

Tests opposite direction of Exp 017 (which biased toward NEXT-in-cycle).
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 25

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)

dist_for_tbase = np.zeros((4, 4))
for t in range(4):
    prev = (t - 1) % 4
    dist_for_tbase[t, t] = 0.7
    dist_for_tbase[t, prev] = 0.2
    for k in range(4):
        if k != t and k != prev:
            dist_for_tbase[t, k] = 0.05
assert np.allclose(dist_for_tbase.sum(axis=1), 1.0)

cum = dist_for_tbase.cumsum(axis=1)
pos_cum = cum[template]
u = rng.random((N, L))
seqs = (u[:, :, None] >= pos_cum[None, :, :]).sum(axis=2).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
pos0_freqs = [(seqs[:, 0] == b).mean() for b in range(4)]
print(f"wrote {N}; pos-0 freqs (expect 0.7/0.05/0.05/0.2) = {[round(x,3) for x in pos0_freqs]}")
