"""Exp 008: random preferred base per position, p=0.7 (no periodicity).

Each of the 200 positions has a fixed randomly-chosen preferred base
(drawn ONCE; same for all 50,000 sequences). Each sequence: at each
position, p=0.7 of the preferred base, 0.1 each of the other 3.

Tests whether the lift in Exp 006 came from period-4 *structure* or
just from any per-position positional bias.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 8
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
template = rng.integers(0, 4, size=L, dtype=np.uint8)  # random per-position
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
print(f"wrote {N}; template first 20 = {template[:20].tolist()}")
print(f"unique sequences: {len(set(map(bytes, seqs)))}")
