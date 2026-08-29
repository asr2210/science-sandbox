"""4 buckets of compositionally-biased seqs:
Bucket k: each char drawn iid with P(k)=0.85, P(other)=0.05 each.
Tests if heavily biased per-seq compositions, grouped by 4 distinct types,
trigger response."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
HEAVY = 0.85

with open("libraries/006_buckets_biased_compo/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
