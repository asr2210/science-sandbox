"""014_gradient_min1 — push composition gradient endpoints to min count = 1.
Same det-counts + random-shuffle structure as 009 but more extreme:
row 0:   counts (1, 99, 99, 1)
row N-1: counts (99, 1, 1, 99)
"""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(606)
out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c_at = int(round(1 + 98 * frac))
    c_gc = 100 - c_at
    chars = [0]*c_at + [1]*c_gc + [2]*c_gc + [3]*c_at
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} gradient strings (min count 1) to {out}")
