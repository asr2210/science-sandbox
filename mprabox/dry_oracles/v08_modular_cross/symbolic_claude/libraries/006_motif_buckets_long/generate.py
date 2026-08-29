"""Experiment 006: Long-motif buckets (motif length 100).

Same 4-bucket layout as exp 005, but the poly-X motif now occupies
positions 50-149 (100 chars) instead of 90-109 (20 chars). Background
(positions 0-49 and 150-199) remains random per string.

If the modest +0.006 mean_r in exp 005 came from motif/bucket signal,
amplifying the motif should multiply the effect.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 100
MOTIF_START = 50
rng = np.random.default_rng(seed=37)

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
