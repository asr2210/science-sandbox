"""Experiment 015: 4 buckets with background enriched for the bucket char.

Like exp 005 (4 buckets, poly-X motif length 20 at pos 90), but background
is biased: 50% bucket char + 50/3 % each of the other 3 chars (uniform
among them). The motif region remains pure poly-X.

If signal increases vs exp 005, compositional contrast across buckets
amplifies the predictor's per-string response. If similar or lower,
the motif itself was driving the signal.
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
        # Probabilities: 0.5 for bucket char, 0.5/3 for others
        probs = np.full(4, 0.5 / 3)
        probs[bucket] = 0.5
        bg = rng.choice(4, size=(N_BUCKET, STR_LEN), p=probs).astype(np.uint8)
        for row in bg:
            chars = bytearray(ord('0') + int(c) for c in row)
            for k in range(MOTIF_LEN):
                chars[MOTIF_START + k] = motif_ch
            f.write(chars.decode("ascii") + "\n")
print("done")
