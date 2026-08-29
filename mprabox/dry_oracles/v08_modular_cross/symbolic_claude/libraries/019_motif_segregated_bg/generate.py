"""Experiment 019: poly-X motif at pos 90, bg uniform from {others}.

Each bucket: motif poly-X (length 20) at pos 90 (exp 005), BUT background
draws uniformly from the 3 OTHER characters (the bucket char only appears
in the motif region).

Tests whether motif segregation strengthens the position-specific signal
detected by the predictor. If signal increases vs exp 5 (0.0061), the
predictor benefits from having the motif char appear *only* in the motif
region.
"""
import os
import numpy as np

N_BUCKET = 12_500
STR_LEN = 200
MOTIF_LEN = 20
MOTIF_START = 90
rng = np.random.default_rng(seed=23)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for bucket in range(4):
        motif_ch = ord('0') + bucket
        # bg chars: all except bucket
        bg_choices = np.array([c for c in range(4) if c != bucket],
                              dtype=np.uint8)
        bg = rng.choice(bg_choices, size=(N_BUCKET, STR_LEN)).astype(np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
