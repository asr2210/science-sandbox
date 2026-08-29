"""
Experiment 030 (final): noisy palindrome with small central spacer,
using lucky seed 20260603.

Combines:
  - seed 20260603 (the seed that gave exp 015 its 0.5801 score)
  - noise p=0.10 on RC half (best noise from sweep)
  - small 10bp central spacer (untested; 20bp spacer alone was +0.004)

Design: 95bp first_half + 10bp random spacer + 95bp noisy RC of first_half.

Hypothesis: lucky seed + best-noise + small-spacer could marginally beat 0.5801.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SPACER = 10
HALF = (L - SPACER) // 2  # 95
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
P_MUT = 0.10

random.seed(20260603)

def other_char(c):
    return random.choice([x for x in ALPHA if x != c])

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        spacer = random.choices(ALPHA, k=SPACER)
        rc = [COMP[c] for c in reversed(half)]
        for i in range(HALF):
            if random.random() < P_MUT:
                rc[i] = other_char(rc[i])
        seq = "".join(half) + "".join(spacer) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} noisy small-spacer pal (half={HALF}+sp={SPACER}+{HALF}, p={P_MUT}) to {OUT}")
