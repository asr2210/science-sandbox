"""AT-rich random: 35% GC, 65% AT."""
import numpy as np

N, L = 50000, 200
rng = np.random.default_rng(3)
probs = np.array([0.325, 0.175, 0.175, 0.325])  # A C G T
alphabet = np.array(list("ACGT"))
idx = rng.choice(4, size=(N, L), p=probs)
seqs = alphabet[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} GC35 sequences")
