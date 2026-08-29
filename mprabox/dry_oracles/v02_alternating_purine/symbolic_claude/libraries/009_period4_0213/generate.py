"""Exp 009: period-4 motif 0,2,1,3 (alternative permutation) at p=0.7.

Same setup as Exp 006 (period 4, p=0.7) but the motif is "0,2,1,3"
instead of "0,1,2,3". Each base still preferred at 1/4 of positions.
Tests whether the *specific* permutation matters.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 9
P_TEMPLATE = 0.7
MOTIF = np.array([0, 2, 1, 3], dtype=np.uint8)

rng = np.random.default_rng(SEED)
template = MOTIF[np.arange(L) % 4]  # period 4
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
print(f"wrote {N}; motif = 0,2,1,3 repeating; unique = {len(set(map(bytes, seqs)))}")
