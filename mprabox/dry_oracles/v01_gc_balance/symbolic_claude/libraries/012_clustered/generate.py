"""012_clustered — same composition gradient as 009 but with intra-row
clustering (sorted) + row-dependent cyclic shift to maintain column variance.
"""
import os, numpy as np
N, L = 50_000, 200

out_lines = []
for i in range(N):
    frac = i / (N - 1)
    c_at = int(round(2 + 96 * frac))
    c_gc = 100 - c_at
    sorted_row = "0"*c_at + "1"*c_gc + "2"*c_gc + "3"*c_at
    assert len(sorted_row) == L
    # row-dependent cyclic shift
    offset = (i * 113) % L
    shifted = sorted_row[-offset:] + sorted_row[:-offset]
    out_lines.append(shifted)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_lines) + "\n")
print(f"Wrote {N} clustered+shifted rows to {out}")
