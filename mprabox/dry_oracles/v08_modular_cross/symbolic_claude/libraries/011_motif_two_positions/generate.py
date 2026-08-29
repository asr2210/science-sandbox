"""Experiment 011: Bucketed motif at TWO positions (50 and 90).

Each string has the bucket's poly-X motif duplicated at two positions:
positions 50-69 AND positions 90-109. 40 chars motif total, 160 random.

This tests whether multi-positional motifs amplify the signal vs single
position (exp 005). If condition_a / mean_r increase for eval_01, more
copies help.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_POSITIONS = [50, 90]
rng = np.random.default_rng(seed=23)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket in range(4):
        motif_ch = ord('0') + bucket
        bg = rng.integers(0, 4, size=(N_BUCKET, STR_LEN), dtype=np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for start in MOTIF_POSITIONS:
                for k in range(MOTIF_LEN):
                    chars[start + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
