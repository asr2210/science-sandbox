"""Exp 018: period-4 (0,1,2,3) at p=0.75."""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 18
P_TEMPLATE = 0.75

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
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
print(f"wrote {N}; pos-0 base-0 freq = {(seqs[:,0]==0).mean():.3f}")
