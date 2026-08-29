"""
Experiment 004: Autocorrelation / structure probe.

50,000 sequences from a 1st-order Markov chain with permutation-symmetric
transitions:
    P(c_t = c_{t-1})       = 0.5
    P(c_t = c')  for c' != c_{t-1} = 1/6 each

Stationary distribution is uniform (25/25/25/25 per position), matching
the baseline composition. The only difference from uniform random is
that dinucleotides are non-uniform: same-char dinucleotides at P=0.5,
each other dinucleotide at P=1/6.

If structure (autocorrelation) HELPS the score, mean_r > baseline.
If high local entropy HELPS, mean_r < baseline.
If only per-position composition matters, mean_r ≈ baseline.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"

P_SAME = 0.5
P_DIFF = (1.0 - P_SAME) / 3  # 1/6

random.seed(20260603)

def transition(prev):
    if random.random() < P_SAME:
        return prev
    others = [c for c in ALPHA if c != prev]
    return random.choice(others)

with open(OUT, "w") as f:
    for _ in range(N):
        seq = [random.choice(ALPHA)]
        for _ in range(L - 1):
            seq.append(transition(seq[-1]))
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
