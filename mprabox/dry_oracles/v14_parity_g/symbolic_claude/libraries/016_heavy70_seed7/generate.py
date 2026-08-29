"""Seed lottery: HEAVY=0.7 4 buckets, seed=7 (best config so far)."""
import numpy as np

rng = np.random.default_rng(7)
N_BUCKET = 12_500
L = 200
HEAVY = 0.7

with open("libraries/016_heavy70_seed7/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
