"""Experiment 010: Same 4-bucket motif as exp 005 but motif at pos 0.

Tests whether the position of the motif within the string matters.
exp 005 had motif at pos 90 (middle). Here motif at pos 0 (start).

If mean_r differs significantly from 005, motif POSITION is a factor.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 0
rng = np.random.default_rng(seed=23)

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
