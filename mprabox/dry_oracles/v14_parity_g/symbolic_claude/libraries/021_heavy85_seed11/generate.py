"""HEAVY=0.85 4 blocked buckets seed=11. Seed lottery."""
import numpy as np

rng = np.random.default_rng(11)
N_BUCKET = 12_500
L = 200
HEAVY = 0.85

with open("libraries/021_heavy85_seed11/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
