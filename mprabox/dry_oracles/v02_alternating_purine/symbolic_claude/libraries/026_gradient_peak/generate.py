"""Exp 026: period-4 phase 0 with GRADIENT peak shape.

Per position i (template = i mod 4):
- template: 0.5
- prev-in-cycle ((i-1) mod 4): 0.2
- next-in-cycle ((i+1) mod 4): 0.2
- antipodal ((i+2) mod 4): 0.1

Symmetric (both prev and next at 0.2). Soft gradient peak shape.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 26

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)

dist_for_tbase = np.zeros((4, 4))
for t in range(4):
    prev = (t - 1) % 4
    nxt = (t + 1) % 4
    anti = (t + 2) % 4
    dist_for_tbase[t, t] = 0.5
    dist_for_tbase[t, prev] = 0.2
    dist_for_tbase[t, nxt] = 0.2
    dist_for_tbase[t, anti] = 0.1
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
print(f"wrote {N}; pos-0 freqs (expect 0.5/0.2/0.1/0.2) = {[round(x,3) for x in pos0_freqs]}")
