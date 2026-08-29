"""Same as 009 ([43,57] uniform-over-tuples + shuffle) but with seed=7.
Measures sampling noise around 009's 0.8820 estimate.
If 019 ≈ 0.882: my measurements are stable, 009 is a robust local optimum.
If 019 differs significantly: noise is large; rankings may be unreliable."""
import os
import numpy as np

rng = np.random.default_rng(7)  # different seed
N, L = 50000, 200
LO, HI = 43, 57

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
print(f"wrote {N} sequences (seed=7)")
