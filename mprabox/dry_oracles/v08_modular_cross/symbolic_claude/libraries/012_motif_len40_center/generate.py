"""Experiment 012: motif length 40 centered (pos 80-119), 4 buckets.

Brackets the length sweet spot: exp 005 had len 20 (+0.0061) and
exp 006 had len 100 (+0.0029). Test len 40 centered. If signal is
similar to or better than exp 005, longer-centered is OK; if worse,
length 20 was specifically tuned.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 40
MOTIF_START = 80
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
