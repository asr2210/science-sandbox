"""Experiment 008: Motifs interleaved (alternating per string).

Same per-string structure as exp 005 (poly-X motif length 20 at pos 90-109,
random uniform background) but the motif identity now cycles as i % 4
rather than being bucketed.

Compares to exp 005 (forward buckets, +0.006) and 007 (reverse buckets,
+0.002). If interleaving yields ~0, then library-order structure was the
driver. If still positive, motif diversity is the driver.
"""
import os
import numpy as np

N_STRINGS = 50_000
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)  # same seed as 005/007 for parity

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
bg = rng.integers(0, 4, size=(N_STRINGS, STR_LEN), dtype=np.uint8)
with open(out_path, "w") as f:
    for i, row in enumerate(bg):
        chars = bytearray(ord('0') + int(c) for c in row)
        motif_ch = ord('0') + (i % 4)
        for k in range(MOTIF_LEN):
            chars[MOTIF_START + k] = motif_ch
        f.write(chars.decode("ascii") + "\n")
print("done")
