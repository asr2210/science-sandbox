"""Exp 020: per-sequence random phase period-4 at p=0.7.

Each sequence picks phase ∈ {0,1,2,3} independently, then uses
(phase + i) mod 4 as its template. Library covers all phases.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 20
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
phases = rng.integers(0, 4, size=N, dtype=np.uint8)        # (N,)
positions = np.arange(L, dtype=np.uint8)                   # (L,)
template_tile = ((phases[:, None] + positions[None, :]) % 4).astype(np.uint8)  # (N, L)

keep_mask = rng.random((N, L)) < P_TEMPLATE
rand_alt = rng.integers(0, 3, size=(N, L), dtype=np.uint8)
alt = (template_tile + 1 + rand_alt) % 4
seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min base count per position = {min(mins)}")
