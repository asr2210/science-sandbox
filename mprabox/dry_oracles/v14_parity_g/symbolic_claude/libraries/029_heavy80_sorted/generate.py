"""4 buckets HEAVY=0.80 seed=42, rows within each block sorted ascending
by dominant-char count. Hypothesis: this stabilizes seed-dependent cond_b
signal and may boost it."""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 12_500
L = 200
HEAVY = 0.80

with open("libraries/029_heavy80_sorted/sequences_0.txt", "w") as f:
    for k in range(4):
        probs = np.full(4, (1.0 - HEAVY) / 3)
        probs[k] = HEAVY
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        # count of dominant char k per row
        counts = (bg == k).sum(axis=1)
        # ascending: rows with fewer of char k come first
        order = np.argsort(counts, kind="stable")
        bg = bg[order]
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
