"""
Experiment 003: Composition probe with diversity preserved.

Four sub-libraries of 12,500 sequences each, drawn iid per-position from
a Categorical with one character at probability 0.55 and the other three
at 0.15 each. Total 50,000 distinct (with overwhelming probability)
sequences.

The 55% bias is mild enough to preserve full intra-sequence variance
(no constant runs across length 200), so the score should not return
NaN from monochromatic degeneracy.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
L = 200
PER = 12_500
ALPHA = "0123"

random.seed(20260603)

with open(OUT, "w") as f:
    for biased_char in ALPHA:
        weights = [0.15] * 4
        weights[int(biased_char)] = 0.55
        for _ in range(PER):
            f.write("".join(random.choices(ALPHA, weights=weights, k=L)))
            f.write("\n")

print(f"Wrote {4*PER} sequences of length {L} to {OUT}")
