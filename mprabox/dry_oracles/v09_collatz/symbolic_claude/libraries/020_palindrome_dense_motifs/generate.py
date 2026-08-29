"""Palindrome + 24 scaffold + tail of dense palindromic 4-mers.

Left half:
- Positions 0-23: scaffold "012301230123 012301230123" (period-4,
  self-RC-palindromic)
- Positions 24-99: 19 random palindromic 4-mers concatenated
  (each from the 8 balanced palindromic 4-mers, so composition stays
  balanced)
Right half: RC of left half.

Total LOCAL palindromic content (per sequence) is much higher than
exp 014. b might see more palindrome density and reward more.
"""
import numpy as np
import os

rng = np.random.default_rng(2020)
N, L = 50000, 200

# 8 balanced RC-palindromic 4-mers (a from one comp-pair, b from the
# other; comp 0<->3, 1<->2). Each motif is "a b comp(b) comp(a)".
balanced_4mers = np.array([
    [0, 1, 2, 3],
    [0, 2, 1, 3],
    [3, 1, 2, 0],
    [3, 2, 1, 0],
    [1, 0, 3, 2],
    [1, 3, 0, 2],
    [2, 0, 3, 1],
    [2, 3, 0, 1],
], dtype=np.uint8)

SCAF_LEN = 24
scaffold = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)
HALF = L // 2
TAIL = HALF - SCAF_LEN  # 76
N_4MERS = TAIL // 4     # 19

# For each sequence, pick N_4MERS palindromic 4-mers
choices = rng.integers(0, len(balanced_4mers), size=(N, N_4MERS))
tail_4mers = balanced_4mers[choices]  # (N, N_4MERS, 4)
tail = tail_4mers.reshape(N, N_4MERS * 4)  # (N, 76)
assert tail.shape == (N, TAIL)

left = np.empty((N, HALF), dtype=np.uint8)
left[:, :SCAF_LEN] = scaffold
left[:, SCAF_LEN:] = tail
right = (3 - left).astype(np.uint8)[:, ::-1]
arr = np.concatenate([left, right], axis=1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
unique, counts = np.unique(arr, return_counts=True)
print("composition:", {int(u): float(c) / arr.size for u, c in zip(unique, counts)})
