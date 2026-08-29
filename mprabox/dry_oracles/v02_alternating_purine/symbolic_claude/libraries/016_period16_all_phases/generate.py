"""Exp 016: period-16 template covering all 4 phases of (0,1,2,3).

Template: (0,1,2,3, 1,2,3,0, 2,3,0,1, 3,0,1,2). Each 4-position block
is a different phase of (0,1,2,3). p_template=0.7.

Hypothesis: different evals reward different phases of period-4;
a multi-phase template might lift mean across multiple evals.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 16
P_TEMPLATE = 0.7
MOTIF = np.array([0,1,2,3, 1,2,3,0, 2,3,0,1, 3,0,1,2], dtype=np.uint8)

rng = np.random.default_rng(SEED)
template = MOTIF[np.arange(L) % 16]
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
print(f"wrote {N}; motif first 16 = {MOTIF.tolist()}; unique={len(set(map(bytes, seqs)))}")
