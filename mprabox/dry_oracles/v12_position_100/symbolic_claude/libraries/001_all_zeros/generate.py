"""Exp 001: all-zero baseline. 50,000 identical strings of '0'*200."""
import os

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

with open(OUT, "w") as f:
    line = "0" * L + "\n"
    for _ in range(N):
        f.write(line)

print(f"wrote {N} lines to {OUT}")
