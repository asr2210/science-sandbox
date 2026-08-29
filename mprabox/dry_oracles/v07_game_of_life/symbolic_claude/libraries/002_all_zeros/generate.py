"""Experiment 002: all-zero constant strings."""
import os

N = 50_000
L = 200
seq = "0" * L

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(seq)
        f.write("\n")
print(f"Wrote {N} copies of '{seq[:8]}...' to {out_path}")
