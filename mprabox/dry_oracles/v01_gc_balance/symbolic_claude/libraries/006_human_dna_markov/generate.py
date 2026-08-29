"""
Experiment 006: DNA-like Markov chain.

50K sequences from Markov-1 with transition probabilities derived from
approximate human dinucleotide frequencies, assuming the alphabet
mapping {0,1,2,3} = {A,C,G,T}.

If the score rewards "biologically realistic" sequences, this should
beat uniform random (0.485). If r drops or stays roughly the same,
then biological realism is not what the scoring tracks — uniform
random is approximately the global optimum for this score.

Dinucleotide frequencies (approximate, from human genome):
  AA AC AG AT  CA CC CG CT  GA GC GG GT  TA TC TG TT
  .080 .054 .072 .092  .073 .054 .014 .072
  .060 .043 .054 .054  .065 .060 .073 .080

Mapping:
  A = 0, C = 1, G = 2, T = 3
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"

# Dinucleotide frequencies, indexed by (i, j) where i is prev char and j is next.
# Order: row = prev (A,C,G,T), col = next (A,C,G,T)
DINUC = [
    [0.080, 0.054, 0.072, 0.092],  # A -> *
    [0.073, 0.054, 0.014, 0.072],  # C -> *
    [0.060, 0.043, 0.054, 0.054],  # G -> *
    [0.065, 0.060, 0.073, 0.080],  # T -> *
]

# Convert to transition probabilities P(j | i) = freq(i,j) / sum_j freq(i,j)
TRANS = []
for row in DINUC:
    s = sum(row)
    TRANS.append([p / s for p in row])

# Stationary distribution (we can solve, or just compute from sums of dinucs):
# Approximate stationary marginals (sum over j of freq(i,j)) — slightly
# non-uniform due to underlying data. We'll use these to seed first char.
STATIONARY = [sum(row) for row in DINUC]
s = sum(STATIONARY)
STATIONARY = [p / s for p in STATIONARY]
# Approx ~0.298, 0.213, 0.211, 0.278 — AT-leaning, GC-depressed.

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        # Sample first character from stationary
        c = random.choices(range(4), weights=STATIONARY, k=1)[0]
        seq = [str(c)]
        for _ in range(L - 1):
            c = random.choices(range(4), weights=TRANS[c], k=1)[0]
            seq.append(str(c))
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
print(f"Stationary: {[round(x, 3) for x in STATIONARY]}")
print(f"Trans from A: {[round(x, 3) for x in TRANS[0]]}")
print(f"Trans from C: {[round(x, 3) for x in TRANS[1]]}")
