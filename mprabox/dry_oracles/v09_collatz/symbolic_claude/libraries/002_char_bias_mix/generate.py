"""Generate 50,000 sequences split into 4 groups of 12,500.

Each group is iid with one character heavily biased to 70% and the
others at 10% each. Lets us see whether the scorer cares about
composition, while keeping within-library variance (Pearson r safe).
"""
import numpy as np
import os

rng = np.random.default_rng(202)
N_PER = 12500
L = 200

parts = []
for biased_char in range(4):
    probs = np.full(4, 0.10)
    probs[biased_char] = 0.70
    arr = rng.choice(4, size=(N_PER, L), p=probs).astype(np.uint8)
    parts.append(arr)

all_arr = np.vstack(parts)
# shuffle so groups are interleaved
perm = rng.permutation(all_arr.shape[0])
all_arr = all_arr[perm]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in all_arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {all_arr.shape[0]} sequences to {out_path}")
