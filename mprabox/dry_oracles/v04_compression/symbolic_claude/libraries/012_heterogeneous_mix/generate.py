"""Heterogeneous mixture: 4 subsets of 12,500, each with a different
single-char bias (50%/16.7%/16.7%/16.7%). Tests if a library with
diverse per-seq composition skews helps oracle response variance.
"""
import os, random
random.seed(42)

L = 200
N_per = 12500
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

def biased_seq(bias_char, p_bias=0.5):
    rest = [c for c in "0123" if c != bias_char]
    other_p = (1 - p_bias) / 3
    weights = [p_bias if c == bias_char else other_p for c in "0123"]
    return "".join(random.choices("0123", weights=weights, k=L))

with open(out_path, "w") as f:
    for bias in "0123":
        for _ in range(N_per):
            f.write(biased_seq(bias) + "\n")
print("wrote 4x12500 with biased compositions 50% per char")
