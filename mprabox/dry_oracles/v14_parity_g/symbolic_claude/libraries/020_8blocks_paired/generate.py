"""8 blocked buckets, chars (0,0,1,1,2,2,3,3) - each pair of blocks shares bias.
Tests whether target's block boundaries align with 4 or 8 blocks."""
import numpy as np

rng = np.random.default_rng(42)
N_BLOCK = 6250
L = 200
HEAVY = 0.85
chars = [0, 0, 1, 1, 2, 2, 3, 3]

with open("libraries/020_8blocks_paired/sequences_0.txt", "w") as f:
    for k in chars:
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BLOCK, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
