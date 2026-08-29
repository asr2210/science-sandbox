"""Experiment 005: 41% GC i.i.d., approximating real human genome composition."""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))
# A:T:C:G = 0.295:0.295:0.205:0.205 → GC=0.41
P = np.array([0.295, 0.205, 0.205, 0.295])

rng = np.random.default_rng(5)
idx = rng.choice(4, size=(N, L), p=P)
seqs = ["".join(ALPHABET[row]) for row in idx]

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
