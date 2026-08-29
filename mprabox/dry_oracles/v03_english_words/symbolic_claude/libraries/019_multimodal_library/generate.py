"""Experiment 019: multimodal library.

Each sequence gets its own composition drawn from a discrete mixture:
- 5000 seqs with p_0=0.20  (under-0 mode)
- 5000 seqs with p_0=0.25
- 30000 seqs with p_0=0.30 (best known)
- 5000 seqs with p_0=0.35
- 5000 seqs with p_0=0.40
For each, the other 3 chars share the remaining mass equally.

Library-level mean p_0 ≈ 0.30 (matches exp 011 mean). But composition VARIES across seqs.

This should boost condition c (composition variance across library) while keeping
a, b near optimum. If the score is composition-variance-rewarded as I observed,
this should beat 0.4272.
"""
import numpy as np

N = 50_000
L = 200
rng = np.random.default_rng(42)

# distribution of p_0 across library
p_0_values = np.array([0.20, 0.25, 0.30, 0.35, 0.40])
counts = np.array([5000, 5000, 30000, 5000, 5000])  # sums to 50000

sequences = []
for p0, count in zip(p_0_values, counts):
    p_rest = (1.0 - p0) / 3.0
    p = np.array([p0, p_rest, p_rest, p_rest])
    # add tiny correction so sums to 1 exactly
    p[3] = 1.0 - p[0] - p[1] - p[2]
    arr = rng.choice(4, size=(count, L), p=p).astype(np.uint8)
    sequences.append(arr)

all_seqs = np.vstack(sequences)
# shuffle so order doesn't matter
shuffled = rng.permutation(all_seqs)

with open("sequences_0.txt", "w") as f:
    for row in shuffled:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")

print(f"Wrote {N} sequences of length {L}, multimodal p_0 distribution")
print(f"Library mean p_0: {np.average(p_0_values, weights=counts):.4f}")
