"""Experiment 004: Periodic template test (4 different templates).

Tests if scoring rewards alignment with periodic templates.
4 blocks of 12,500 each, testing 4 different periodic templates with 30% noise.
"""
import os
import numpy as np

N_PER_BLOCK = 12_500
L = 200
SEED = 11
NOISE = 0.3

templates = []
templates.append([i % 4 for i in range(L)])              # period 4: 0,1,2,3
templates.append([(i // 2) % 4 for i in range(L)])       # period 8: 00,11,22,33
templates.append([i % 2 for i in range(L)])              # period 2: 0,1
templates.append([(i // 50) % 4 for i in range(L)])      # block-of-50: 50x0,50x1,50x2,50x3

rng = np.random.default_rng(SEED)
out_lines = []
for template in templates:
    template = np.array(template, dtype=np.uint8)
    block = np.broadcast_to(template, (N_PER_BLOCK, L)).copy()
    # Pick noise positions in batch
    noise_mask = rng.random((N_PER_BLOCK, L)) < NOISE
    # For noise positions, replace with one of the 3 other chars
    # Generate random integers in 0..2; map to non-template values.
    noise_offset = rng.integers(1, 4, size=(N_PER_BLOCK, L), dtype=np.uint8)
    replaced = (block + noise_offset) % 4
    block = np.where(noise_mask, replaced, block)
    for row in block:
        out_lines.append("".join(map(str, row.tolist())))

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote 4 template blocks of {N_PER_BLOCK} to {out_path}")
