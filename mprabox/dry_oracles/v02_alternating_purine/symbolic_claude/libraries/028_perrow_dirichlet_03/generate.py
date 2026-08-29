"""Exp 028: per-row Dirichlet(0.3) noise direction — sharper per-row.

Same as Exp 027 but Dirichlet(0.3) makes per-row noise weights more
extreme (often near-deterministic single direction). Tests if more
per-row concentration continues to lift c.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 28
P_TEMPLATE = 0.7
ALPHA = 0.3

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
template_tile = np.broadcast_to(template, (N, L))

noise_weights = rng.dirichlet(np.full(3, ALPHA), size=N)
noise_cum = noise_weights.cumsum(axis=1)

keep_mask = rng.random((N, L)) < P_TEMPLATE
u = rng.random((N, L))
offset = (u[:, :, None] >= noise_cum[:, None, :]).sum(axis=2) + 1
alt = (template_tile + offset.astype(np.uint8)) % 4

seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min base count per position = {min(mins)}")
