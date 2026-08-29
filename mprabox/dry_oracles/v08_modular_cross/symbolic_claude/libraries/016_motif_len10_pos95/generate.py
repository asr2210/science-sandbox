"""Experiment 016: motif length 10 at pos 95, 4 buckets.

Tests whether shorter motif (length 10) improves on exp 005 (length 20).
If higher → continue shrinking. If lower → length 20 is the sweet spot.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 10
MOTIF_START = 95
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
