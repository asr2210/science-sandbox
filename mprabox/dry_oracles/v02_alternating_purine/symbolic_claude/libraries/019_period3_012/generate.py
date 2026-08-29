"""Exp 019: period-3 (0,1,2) at p=0.7.

Template = (0,1,2) repeated. Tests whether period-4 is strictly required.
All 4 bases appear library-wide (base 3 only via noise) so no NaN.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 19
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
motif = np.array([0, 1, 2], dtype=np.uint8)
template = motif[np.arange(L) % 3]
template_tile = np.broadcast_to(template, (N, L))

keep_mask = rng.random((N, L)) < P_TEMPLATE
rand_alt = rng.integers(0, 3, size=(N, L), dtype=np.uint8)
alt = (template_tile + 1 + rand_alt) % 4
seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
# sanity: at each position, all 4 bases must appear (otherwise NaN)
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min count per base across positions = {min(mins)}")
