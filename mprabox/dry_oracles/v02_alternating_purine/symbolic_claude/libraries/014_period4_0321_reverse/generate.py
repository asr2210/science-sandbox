"""Exp 014: period-4 motif (0,3,2,1) — reverse-orbit of (0,1,2,3) — at p=0.7.

Tests whether descending ordering scores similarly to ascending.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 14
P_TEMPLATE = 0.7
MOTIF = np.array([0, 3, 2, 1], dtype=np.uint8)

rng = np.random.default_rng(SEED)
template = MOTIF[np.arange(L) % 4]
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
print(f"wrote {N}; motif={MOTIF.tolist()} repeating; unique={len(set(map(bytes, seqs)))}")
