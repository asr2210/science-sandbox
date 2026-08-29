"""Experiment 002: 4-way constant-character probe.

50,000 strings split into 4 groups of 12,500:
- All-zero strings  (12,500)
- All-one strings   (12,500)
- All-two strings   (12,500)
- All-three strings (12,500)

If composition (or character identity) matters, mean should deviate from 0.
"""
import os

N_PER = 12_500
L = 200

lines = []
for ch in "0123":
    lines.extend([ch * L] * N_PER)

# don't shuffle — preserve interpretability; per-string scoring is invariant
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {len(lines)} sequences (12500 each of all-0,1,2,3)")
