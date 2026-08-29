"""4 buckets HEAVY=0.85 blocked, but char permutation REVERSED.
bucket 0 (rows 0-12499) biases toward char 3, bucket 1 -> 2, bucket 2 -> 1, bucket 3 -> 0.
Tests whether specific char assignment matters or only block structure."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
HEAVY = 0.85
char_for_bucket = [3, 2, 1, 0]

with open("libraries/018_heavy85_perm_reversed/sequences_0.txt", "w") as f:
    for bucket_idx in range(4):
        k = char_for_bucket[bucket_idx]
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
