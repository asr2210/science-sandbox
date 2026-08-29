"""
Experiment 005: Anti-correlation probe.

50,000 Markov-1 sequences with P(c_t = c_{t-1}) = 0. Every consecutive
pair MUST differ; each non-same transition has P = 1/3. Per-position
marginals are uniform 25/25/25/25.

This is the opposite of exp 004 along the same dinucleotide axis.
- If r > baseline (0.485): anti-correlation helps; high-entropy wins.
- If r < baseline: any deviation from uniform-random dinucleotide hurts.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
ALPHA = "0123"

random.seed(20260603)

with open(OUT, "w") as f:
    for _ in range(N):
        seq = [random.choice(ALPHA)]
        for _ in range(L - 1):
            others = [c for c in ALPHA if c != seq[-1]]
            seq.append(random.choice(others))
        f.write("".join(seq))
        f.write("\n")

print(f"Wrote {N} sequences of length {L} to {OUT}")
