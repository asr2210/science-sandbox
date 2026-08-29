"""Experiment 020: 4 buckets, poly-X motif length 20 at pos 85-104.

Slight shift LEFT from exp 005 (pos 90). Combined with exp 018 (pos 100,
0.0001) tells us if the position optimum is sharp at 90 (pos 85 also bad)
or broad on the left side.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 85
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
