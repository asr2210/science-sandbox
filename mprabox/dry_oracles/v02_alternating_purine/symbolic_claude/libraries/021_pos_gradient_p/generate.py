"""Exp 021: positional gradient p — high at start, low at end.

p=0.95 for positions 0-99, p=0.5 for positions 100-199. Period-4 phase 0.
Tests positional weighting of eval.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 21

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)
template_tile = np.broadcast_to(template, (N, L))

# Position-dependent p
p_per_pos = np.where(np.arange(L) < 100, 0.95, 0.5)        # (L,)
keep_mask = rng.random((N, L)) < p_per_pos[None, :]
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
