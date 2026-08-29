"""Experiment 002: All-zeros constant.

50,000 identical strings of "0" repeated 200 times. The mean score
will equal the per-string score for "0"*200, giving us a clean data
point on what the function thinks of the simplest possible structure.
"""
import os

N = 50_000
L = 200

seq = "0" * L

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(seq + "\n")

print(f"Wrote {N} sequences (all '0'*{L}) to {out_path}")
