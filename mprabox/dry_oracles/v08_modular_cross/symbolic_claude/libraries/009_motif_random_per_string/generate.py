"""Experiment 009: Random motif identity per string (period = 1).

Each string i: random uniform background, poly-X motif length 20 at
pos 90, where X is randomly drawn per string from {0,1,2,3}.

Compared to interleaved (period 4, condition_a 0.0107) and bucketed
(period 12500, condition_a 0.0060). If condition_a goes higher,
target-prediction matching benefits from fully-random motif assignment.
"""
import os
import numpy as np

N_STRINGS = 50_000
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

bg = rng.integers(0, 4, size=(N_STRINGS, STR_LEN), dtype=np.uint8)
motif_chars = rng.integers(0, 4, size=N_STRINGS, dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N_STRINGS):
        row = bg[i]
        chars = bytearray(ord('0') + int(c) for c in row)
        m = ord('0') + int(motif_chars[i])
        for k in range(MOTIF_LEN):
            chars[MOTIF_START + k] = m
        f.write(chars.decode("ascii") + "\n")
print("done")
