"""Same SET of sequences as 003, but with the rows shuffled randomly.

Tests whether ORDER matters. If mean_r ≈ 003 result (-0.005), composition matters.
If mean_r ≈ 0, order matters.
"""
import os
import random

SRC = os.path.join(os.path.dirname(__file__), "..", "003_gradient_3s", "sequences_0.txt")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

with open(SRC) as f:
    lines = f.readlines()

random.Random(1234).shuffle(lines)

with open(OUT, "w") as f:
    f.writelines(lines)

print(f"Shuffled {len(lines)} sequences → {OUT}")
