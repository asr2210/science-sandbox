"""Experiment 018: 4 buckets, poly-X motif length 20 at pos 100-119.

Slight position shift from exp 005 (pos 90-109). Tests how sharply
tuned the eval_01 predictor is to the motif position. If signal
similar (~0.006), broad tuning. If much different, narrow tuning.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 100
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
