"""004_gc_biased — 50K different random sequences, biased toward chars 1 & 2
(if alphabet = ACGT, this is GC-biased; regulatory-relevant in DNA).
P(0)=P(3)=0.15, P(1)=P(2)=0.35.
"""
import os
import numpy as np

N, L = 50_000, 200
SEED = 7
rng = np.random.default_rng(SEED)
probs = np.array([0.15, 0.35, 0.35, 0.15])
arr = rng.choice(4, size=(N, L), p=probs).astype(np.int8)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for row in arr:
        f.write("".join(str(c) for c in row.tolist()))
        f.write("\n")
print(f"Wrote {N} GC-biased random sequences to {out}")
