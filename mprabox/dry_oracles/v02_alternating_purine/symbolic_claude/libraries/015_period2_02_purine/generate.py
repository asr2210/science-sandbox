"""Exp 015: period-2 template (0,2) at p=0.7 ("alternating purine" hint).

Each position: with prob 0.7 the position is template ({0 at even pos,
2 at odd pos}), else uniform over the other 3 bases.
Library still contains all 4 bases (1 and 3 via noise).
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 15
P_TEMPLATE = 0.7
MOTIF = np.array([0, 2], dtype=np.uint8)

rng = np.random.default_rng(SEED)
template = MOTIF[np.arange(L) % 2]
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
freq = {b: (seqs == b).mean() for b in range(4)}
print(f"wrote {N}; library-wide base freq: {freq}; unique={len(set(map(bytes, seqs)))}")
