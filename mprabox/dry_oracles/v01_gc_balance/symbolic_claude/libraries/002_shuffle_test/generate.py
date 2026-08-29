"""
Experiment 002: Take exp 001's sequences and shuffle row order.

Hypothesis test: does row order matter?
- If scores identical to exp 001 → metric is order-invariant (bag-of-seqs).
- If scores differ → metric is per-row (we're predicting against fixed targets).
"""
import os, random

random.seed(2026)

SRC = os.path.join(os.path.dirname(__file__), "..", "001_probe_strata", "sequences_0.txt")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

with open(SRC) as f:
    lines = [line.rstrip("\n") for line in f]

assert len(lines) == 50000, f"expected 50000 got {len(lines)}"

random.shuffle(lines)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote {len(lines)} shuffled sequences to {OUT}")
