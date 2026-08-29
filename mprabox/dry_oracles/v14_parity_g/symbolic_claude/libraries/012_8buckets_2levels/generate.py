"""8 buckets at 2 HEAVY levels: 4 single-char buckets HEAVY=0.85,
4 single-char buckets HEAVY=0.6. 6250 seqs each."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 6250
L = 200

with open("libraries/012_8buckets_2levels/sequences_0.txt", "w") as f:
    for heavy in [0.85, 0.6]:
        for k in range(4):
            probs = np.full(4, (1.0 - heavy) / 3)
            probs[k] = heavy
            bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
            for row in bg:
                f.write("".join(map(str, row.tolist())) + "\n")
