"""009_gradient_extreme — same structure as 008, push to min count = 2.
Row 0: counts (2, 98, 98, 2). Row 49999: counts (98, 2, 2, 98).
"""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(202)

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c_at = int(round(2 + 96 * frac))   # per AT char (0 and 3)
    c_gc = 100 - c_at                  # per GC char (1 and 2)
    chars = [0]*c_at + [1]*c_gc + [2]*c_gc + [3]*c_at
    assert len(chars) == L
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} extreme-gradient (min=2) to {out}")
