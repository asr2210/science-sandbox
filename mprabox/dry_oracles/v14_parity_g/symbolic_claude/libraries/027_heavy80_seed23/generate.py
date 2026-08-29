"""4 buckets, HEAVY=0.80, seed=23. 3rd seed for lottery."""
import numpy as np

rng = np.random.default_rng(23)
N_BUCKET = 12_500
L = 200
HEAVY = 0.80

with open("libraries/027_heavy80_seed23/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
