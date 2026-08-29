"""
Experiment 021: Noisy spacer-flanked palindrome.

Combines exp 015 (noise) + exp 020 (spacer).
seq = first_half(90bp) + spacer(20bp random) + RC(90bp) with
each RC position mutated p=0.10.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SPACER = 20
HALF = (L - SPACER) // 2  # 90
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

print(f"Wrote {N} noisy spacer-pal (half={HALF}, spacer={SPACER}, p={P_MUT}) to {OUT}")
