"""Exp 002: per-character homopolymer probe (4 chunks of 12,500).

12,500 copies each of "000...", "111...", "222...", "333..." (length 200).
mean_r is then the average homopolymer score. If >> baseline 0.127,
composition matters strongly; if << baseline, homopolymers are bad.
Either way, this single submission orients the next round.
"""
from pathlib import Path

L = 200
PER = 12_500

lines = []
for c in "0123":
    seq = c * L
    lines.extend([seq] * PER)

assert len(lines) == 50_000

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} sequences")
