"""8 buckets all at HEAVY=0.85 total bias.
- 4 single-char buckets: (0.85, 0.05, 0.05, 0.05) cycled
- 4 pair-char buckets: 2 chars at 0.425, 2 chars at 0.075"""
import numpy as np

rng = np.random.default_rng(42)
N_BUCKET = 6250
L = 200

probs_list = []
# 4 single-char
for k in range(4):
    p = np.full(4, 0.05)
    p[k] = 0.85
    probs_list.append(p)
# 4 pair-char (using 4 of 6 pairs for symmetry)
for pair in [(0, 1), (0, 2), (1, 3), (2, 3)]:
    p = np.full(4, 0.075)
    p[pair[0]] = 0.425
    p[pair[1]] = 0.425
    probs_list.append(p)

with open("libraries/013_8buckets_single_pair/sequences_0.txt", "w") as f:
    for probs in probs_list:
        bg = rng.choice(4, size=(N_BUCKET, L), p=probs)
        for row in bg:
            f.write("".join(map(str, row.tolist())) + "\n")
