"""Split scaffold: 48 chars at prefix + 48 chars at suffix (period-4),
104 chars uniform random in the middle. Total alignment = 96 chars
distributed in two blocks each <= the 'safe' length seen in 005/008.
"""
import numpy as np
import os

rng = np.random.default_rng(909)
N, L = 50000, 200
SCAF_LEN = 48
scaffold = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)
assert scaffold.size == SCAF_LEN

arr = np.empty((N, L), dtype=np.uint8)
arr[:, :SCAF_LEN] = scaffold
arr[:, -SCAF_LEN:] = scaffold
mid_len = L - 2 * SCAF_LEN
arr[:, SCAF_LEN:SCAF_LEN + mid_len] = rng.integers(0, 4, size=(N, mid_len), dtype=np.uint8)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
