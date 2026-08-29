"""4 buckets HEAVY=0.80, seed=99. Final lottery play for 30/30."""
import numpy as np

rng = np.random.default_rng(99)
N_BUCKET = 12_500
L = 200
HEAVY = 0.80

with open("libraries/030_heavy80_seed99/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
