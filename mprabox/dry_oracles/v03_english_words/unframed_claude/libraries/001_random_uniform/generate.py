"""Random uniform 25% ACGT baseline."""
import numpy as np

N = 50000
L = 200
rng = np.random.default_rng(0)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L))
seqs = alphabet[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} sequences of length {L}")
