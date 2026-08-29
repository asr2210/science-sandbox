"""Experiment 021: REPLICATE exp 5 (best design) with rng seed 42 not 23.

Tests whether exp 5's 0.0061 eval_01 is a robust ceiling or seed-noise.
If seed 42 also gives ~0.006, the bg randomness doesn't matter much
and we have a real ceiling; if it varies a lot, we should marginalize.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=42)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket in range(4):
        motif_ch = ord('0') + bucket
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
