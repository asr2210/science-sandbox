"""
Experiment 016: Noisy palindromes, mutation rate p=0.20.

Sweeps the noise parameter. Pure palindromes (p=0.00) gave 0.5718;
p=0.10 gave 0.5801. Test p=0.20 to find optimum direction.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
HALF = L // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
P_MUT = 0.20

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
