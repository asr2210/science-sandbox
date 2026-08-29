"""Same library as 009 but sorted by count of '0' character.
DIAGNOSTIC: Pearson r should be invariant to row permutation.
If r changes, the eval uses paired indices (i.e., row order matters).
This would be a HUGE insight enabling targeted optimization."""
import os
import numpy as np

rng = np.random.default_rng(42)
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

chars = np.array(list("0123"))
seqs = []
for _ in range(N):
    c = valid[rng.integers(0, len(valid))]
    seq = np.concatenate([np.full(c[i], chars[i]) for i in range(4)])
    rng.shuffle(seq)
    seqs.append("".join(seq))

# Sort by count of '0'
seqs.sort(key=lambda s: s.count("0"))

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"wrote {N} sorted-by-c0 sequences")
