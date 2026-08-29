"""[44,56] uniform-over-tuples — tighter than 009's [43,57], to bracket the peak."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
LO, HI = 44, 56

valid = []
for c0 in range(LO, HI + 1):
    for c1 in range(LO, HI + 1):
        for c2 in range(LO, HI + 1):
            c3 = L - c0 - c1 - c2
            if LO <= c3 <= HI:
                valid.append((c0, c1, c2, c3))
valid = np.array(valid)
print(f"# valid count tuples: {len(valid)}")

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = np.array(list("0123"))
with open(OUT, "w") as f:
    for _ in range(N):
        c = valid[rng.integers(0, len(valid))]
        seq = np.concatenate([np.full(c[i], chars[i]) for i in range(4)])
        rng.shuffle(seq)
        f.write("".join(seq) + "\n")
print(f"wrote {N} uniform-tuple sequences ([{LO},{HI}])")
