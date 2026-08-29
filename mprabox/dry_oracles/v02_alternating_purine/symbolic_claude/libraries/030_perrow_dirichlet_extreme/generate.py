"""Exp 030 (final): per-row 4-way Dirichlet with MAXIMUM per-row variance.

α=(0.7, 0.1, 0.1, 0.1): mean p=0.7 on template, std~0.32 (precision 1).
Most extreme per-row variation tested.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 30
ALPHA = np.array([0.7, 0.1, 0.1, 0.1])

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
template_tile = np.broadcast_to(template, (N, L))

row_weights = rng.dirichlet(ALPHA, size=N)
row_cum = row_weights.cumsum(axis=1)

u = rng.random((N, L))
offset = (u[:, :, None] >= row_cum[:, None, :]).sum(axis=2)
seqs = ((template_tile + offset.astype(np.uint8)) % 4).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min base count per position = {min(mins)}")
print(f"mean p_row = {row_weights[:,0].mean():.3f}, std = {row_weights[:,0].std():.3f}")
