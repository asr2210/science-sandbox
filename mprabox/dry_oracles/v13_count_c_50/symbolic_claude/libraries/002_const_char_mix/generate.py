"""Exp 002: 4-character constant probe.

Each character gets 12500 identical sequences. Tests:
- Whether the metric reacts to extreme bias / loss of diversity
- The average per-character signal
- Whether identical inputs cause issues (NaN, etc.)
"""
import os

N = 50_000
L = 200
ALPHA = "0123"
per_char = N // len(ALPHA)  # 12500

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for ch in ALPHA:
        s = ch * L
        for _ in range(per_char):
            f.write(s + "\n")
print(f"wrote {N} sequences (4 unique constants, {per_char} copies each)")
