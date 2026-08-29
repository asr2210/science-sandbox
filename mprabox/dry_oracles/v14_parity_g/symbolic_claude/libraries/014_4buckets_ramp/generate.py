"""4 buckets, within each bucket HEAVY varies linearly from 0.5 to 0.95
across the 12500 seqs in the bucket. Combines bucket structure (good for b)
with per-seq compositional gradient (good for c)."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200

with open("libraries/014_4buckets_ramp/sequences_0.txt", "w") as f:
    for k in range(4):
        for j in range(N_BUCKET):
            heavy = 0.5 + 0.45 * (j / (N_BUCKET - 1))
            probs = np.full(4, (1.0 - heavy) / 3)
            probs[k] = heavy
            seq = rng.choice(4, size=L, p=probs)
            f.write("".join(map(str, seq.tolist())) + "\n")
