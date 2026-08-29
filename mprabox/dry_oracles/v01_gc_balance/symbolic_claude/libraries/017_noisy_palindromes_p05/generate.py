"""
Experiment 017: Noisy palindromes, p=0.05.

Sweep: p=0.00 → 0.5718, p=0.10 → 0.5801, p=0.20 → 0.5759.
Test p=0.05 to determine if optimum is between 0 and 0.10
or closer to 0.10.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
P_MUT = 0.05

random.seed(20260603)

def other_char(c):
    return random.choice([x for x in ALPHA if x != c])

with open(OUT, "w") as f:
    for _ in range(N):
        half = random.choices(ALPHA, k=HALF)
        rc = [COMP[c] for c in reversed(half)]
        for i in range(HALF):
            if random.random() < P_MUT:
                rc[i] = other_char(rc[i])
        seq = "".join(half) + "".join(rc)
        f.write(seq)
        f.write("\n")

print(f"Wrote {N} noisy palindromes (p_mut={P_MUT}) of length {L} to {OUT}")
