"""Four-way monoculture: 12500 each of 0,1,2,3 monocultures.
Tests whether library-level variance (without within-string variance) is sufficient,
and whether the scoring features care about character identity."""
import os
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(OUT, "w") as f:
    for c in "0123":
        for _ in range(12500):
            f.write(c * 200 + "\n")
print("wrote 50000 (12500 each of 0/1/2/3 monocultures)")
