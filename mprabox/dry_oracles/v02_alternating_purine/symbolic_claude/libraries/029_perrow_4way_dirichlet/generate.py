"""Exp 029: per-row Dirichlet over all 4 offsets (incl. template).

α = (2.1, 0.3, 0.3, 0.3) — mean p=0.7 on template, std~0.23.
Per-row p AND per-row noise direction both vary.

At each position: sample offset ∈ {0,1,2,3} per row weights,
emit (template + offset) mod 4.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 29
ALPHA = np.array([2.1, 0.3, 0.3, 0.3])

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
template_tile = np.broadcast_to(template, (N, L))

row_weights = rng.dirichlet(ALPHA, size=N)             # (N, 4)
row_cum = row_weights.cumsum(axis=1)                   # (N, 4)

u = rng.random((N, L))                                  # (N, L)
offset = (u[:, :, None] >= row_cum[:, None, :]).sum(axis=2)  # (N, L) in {0,1,2,3}
seqs = ((template_tile + offset.astype(np.uint8)) % 4).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min base count per position = {min(mins)}")
print(f"mean row weight on template: {row_weights[:,0].mean():.3f} (target 0.7)")
print(f"std row weight on template:  {row_weights[:,0].std():.3f}")
