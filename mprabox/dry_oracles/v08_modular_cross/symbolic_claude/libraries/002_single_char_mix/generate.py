"""Experiment 002: Single-character probes for each of {0,1,2,3}.

12500 strings each of all-0, all-1, all-2, all-3. Lets us see if any
single character dominates on average. If mean_r is much higher than
random, single-char sequences are good. If only one digit is favored,
the mean over 4 digits will be ~1/4 of that digit's score.
"""
import os

N_EACH = 12_500
STR_LEN = 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

with open(out_path, "w") as f:
    for ch in "0123":
        line = ch * STR_LEN + "\n"
        for _ in range(N_EACH):
            f.write(line)

print(f"Wrote {4*N_EACH} strings to {out_path}")
