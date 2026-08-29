"""002_all_zero: 50,000 copies of the all-zero string (length 200).

Polar opposite of random: zero diversity, single character. Tests whether
condition_c is a diversity measure (should crash to ~0) and whether composition
affects condition_a/b.
"""
from pathlib import Path

N = 50_000
L = 200
seq = "0" * L

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for _ in range(N):
        f.write(seq)
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
