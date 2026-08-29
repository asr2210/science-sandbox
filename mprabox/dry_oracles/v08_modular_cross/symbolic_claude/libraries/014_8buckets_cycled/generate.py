"""Experiment 014: 8 buckets cycling poly-X (0,1,2,3,0,1,2,3).

Same per-string structure as exp 005 but 8 buckets of 6250 each,
poly-X identities cycling through 0,1,2,3 twice. Compare to:
- exp 005 (4 buckets ×12500): 0.0061
- exp 008 (period 4 interleaved): 0.0053

If 8-bucket cycling scores higher than exp 005, more bucket
transitions help. If lower, 4 buckets is the sweet spot.
"""
import os
import numpy as np

N_BUCKET = 6250
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=29)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket in range(8):
        motif_ch = ord('0') + (bucket % 4)
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
