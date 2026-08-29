"""Experiment 022: Same exp-5 layout but SHARE bg across 4 buckets.

12500 random bg strings drawn once. Each bg is duplicated 4x (once per
bucket), with motif at pos 90-109 overwritten per bucket char. Order:
all bucket-0 strings, then bucket-1, etc.

Goal: eliminate per-bucket bg noise. The only systematic difference
between consecutive bucket blocks is the motif itself. If the predictor's
signal is the motif, we should see a sharper correlation than exp 5.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket in range(4):
        motif_ch = ord('0') + bucket
        for row in bg:  # SAME bg reused per bucket
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
