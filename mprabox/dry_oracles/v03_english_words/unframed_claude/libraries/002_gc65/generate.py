"""GC-rich random: 65% GC, 35% AT, iid per base."""
import numpy as np

N, L = 50000, 200
rng = np.random.default_rng(2)
# P(A)=P(T)=0.175, P(C)=P(G)=0.325
probs = np.array([0.175, 0.325, 0.325, 0.175])
alphabet = np.array(list("ACGT"))
idx = rng.choice(4, size=(N, L), p=probs)
seqs = alphabet[idx]

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()) + "\n")

print(f"Wrote {N} GC65 sequences, mean GC ~ {(probs[1]+probs[2]):.2f}")
