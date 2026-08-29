"""Exp 012: blocked ascending template.

Positions 0-49 prefer base 0, 50-99 prefer 1, 100-149 prefer 2,
150-199 prefer 3. p_template = 0.7. Tests whether *ascending arrangement*
across the sequence is the lever or specifically the period-4 cycle.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 12
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
template = (np.arange(L) // 50).astype(np.uint8)  # 50 of each: 0,0,...,0,1,...
assert template.shape == (L,)
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
print(f"wrote {N}; template chunks: {template[0]},{template[49]},{template[50]},{template[199]}")
print(f"unique seqs: {len(set(map(bytes, seqs)))}")
