"""HEAVY=0.85 4 blocks chars (1,2,3,0) — cyclic shift of original.
Tests whether target is sensitive to specific char-bucket alignment phase."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
HEAVY = 0.85
chars = [1, 2, 3, 0]

with open("libraries/022_heavy85_shift1/sequences_0.txt", "w") as f:
    for k in chars:
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
