"""011_sigmoid_gradient — sigmoid composition gradient vs linear (009).
Same endpoints (counts (2,98,98,2) ↔ (98,2,2,98)) but with steep middle.
"""
import os, numpy as np
N, L = 50_000, 200
K = 10.0  # sigmoid steepness
rng = np.random.default_rng(404)

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    alpha = 1.0 / (1.0 + np.exp(-K * (frac - 0.5)))
    c_at = int(round(2 + 96 * alpha))      # AT char counts (per char)
    c_gc = 100 - c_at                      # GC char counts (per char)
    chars = [0]*c_at + [1]*c_gc + [2]*c_gc + [3]*c_at
    assert len(chars) == L, len(chars)
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} sigmoid-gradient (k={K}) to {out}")
