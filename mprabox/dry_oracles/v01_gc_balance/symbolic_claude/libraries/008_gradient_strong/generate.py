"""008_gradient_strong — stronger gradient, deterministic per-row counts.
Row 0: counts (5, 95, 95, 5)   — extreme GC
Row 49999: counts (95, 5, 5, 95) — extreme AT
Within row, random permutation. Each char ≥ 5 in every row.
"""
import os, numpy as np
N, L = 50_000, 200
rng = np.random.default_rng(99)

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c_at = int(round(5 + 90 * frac))   # count of char 0 (and char 3) each
    c_gc = 100 - c_at                  # count of char 1 (and char 2) each
    # Build row: c_at zeros, c_gc ones, c_gc twos, c_at threes
    chars = (
        [0] * c_at + [1] * c_gc + [2] * c_gc + [3] * c_at
    )
    assert len(chars) == L, (len(chars), L)
    row = np.array(chars, dtype=np.int8)
    rng.shuffle(row)
    out_lines.append("".join(str(c) for c in row.tolist()))

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} strong-gradient sequences (det. counts) to {out}")
