"""Experiment 007: Reverse bucket order from exp 005.

Same as exp 005 (motif length 20 at pos 90-109, mostly random background),
but bucket assignment reversed:
- Bucket 1 (i=0..12499):     poly-'3'
- Bucket 2 (i=12500..24999): poly-'2'
- Bucket 3 (i=25000..37499): poly-'1'
- Bucket 4 (i=37500..49999): poly-'0'

If the +0.006 signal in exp 005 was due to LIBRARY ORDER (target is
monotone in i), reversing should give NEGATIVE mean_r (~-0.006).
If the signal is due to motif identity (e.g. poly-0 is a good motif
anywhere it appears), the score should stay positive.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)  # same seed as 005

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    # Reversed motif order
    for motif_ch in [ord('3'), ord('2'), ord('1'), ord('0')]:
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")

print("done")
