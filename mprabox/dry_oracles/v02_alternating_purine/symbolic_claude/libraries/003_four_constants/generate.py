"""003_four_constants: 12,500 copies each of "0"*200, "1"*200, "2"*200, "3"*200.

Library has 2-bit diversity. Tests whether the scoring correlation is dominated
by bulk single-character composition.
"""
from pathlib import Path

N = 50_000
L = 200
per_bucket = N // 4  # 12,500

lines = []
for ch in "0123":
    lines.extend([ch * L] * per_bucket)
assert len(lines) == N

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for s in lines:
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
