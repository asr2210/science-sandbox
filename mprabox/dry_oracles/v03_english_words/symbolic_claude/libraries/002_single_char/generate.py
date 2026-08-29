"""Experiment 002: single-character probe.

12,500 of each: all-0, all-1, all-2, all-3. Each sequence is one character repeated.
This probes pure composition (no positional info, no k-mer info beyond mono).
"""
N = 50_000
L = 200

with open("sequences_0.txt", "w") as f:
    for c in "0123":
        for _ in range(12_500):
            f.write(c * L)
            f.write("\n")

print(f"Wrote {N} sequences of length {L}")
