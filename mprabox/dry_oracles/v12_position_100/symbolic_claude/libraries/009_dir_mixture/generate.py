"""Exp 009: Mixture of Dir(α) at multiple α values.

12.5K seqs each of Dir(0.1), Dir(0.3), Dir(1.0), Dir(3.0).
Aims to cover the simplex broadly: corners (low α) to center (high α).
"""
import os, numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
PER = N // 4

rng = np.random.default_rng(19)
chars = np.array(list("0123"))

lines = []
for alpha in [0.1, 0.3, 1.0, 3.0]:
    weights = rng.dirichlet([alpha] * 4, size=PER)
    for i in range(PER):
        idx = rng.choice(4, size=L, p=weights[i])
        lines.append("".join(chars[idx]))

# shuffle so positions are mixed across alpha buckets
rng.shuffle(lines)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {N} mixed-alpha seqs")
