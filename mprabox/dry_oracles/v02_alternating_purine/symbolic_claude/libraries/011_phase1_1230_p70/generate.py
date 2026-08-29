"""Exp 011: phase-shifted period-4 (motif 1,2,3,0) at p=0.7.

Same as Exp 006 but the cycle starts at base 1 instead of base 0.
template[i] = (i + 1) % 4. Tests phase sensitivity.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 11
P_TEMPLATE = 0.7
PHASE = 1

rng = np.random.default_rng(SEED)
template = ((np.arange(L) + PHASE) % 4).astype(np.uint8)
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
print(f"wrote {N}; template first 8 = {template[:8].tolist()}")
print(f"unique sequences: {len(set(map(bytes, seqs)))}")
