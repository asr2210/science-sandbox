"""Palindrome + scaffold + LOCAL RC-palindromic 6-mers tiled in tail.

Hypothesis: b rewards RC-palindrome at multiple scales. Add local
RC-palindromic 6-mers to the random tail, on top of the global
length-200 palindrome + 24-char scaffold (exp 014 pattern).

Each 6-mer = [a,b,c, comp(c), comp(b), comp(a)] where comp = 3-x.
a,b,c drawn iid uniform per 6-mer, giving 64 distinct 6-mers.

Tail: 76 positions = 12 full 6-mers (72) + 4 free random padding.
Composition: balanced in expectation (each position is uniform 0-3
across sequences). Avoids exp 020's NaN because each 6-mer's a,b,c
draws give per-position diversity across sequences.
"""
import numpy as np
import os

rng = np.random.default_rng(2525)
N, L = 50000, 200
HALF = L // 2  # 100
SCAF_LEN = 24
TAIL = HALF - SCAF_LEN  # 76
N_6MERS = TAIL // 6     # 12
PAD = TAIL - N_6MERS * 6  # 4

scaffold = np.tile([0, 1, 2, 3], SCAF_LEN // 4).astype(np.uint8)

# Build tail: for each sequence, 12 palindromic 6-mers + 4 random
abc = rng.integers(0, 4, size=(N, N_6MERS, 3), dtype=np.uint8)  # a,b,c per 6-mer
# 6-mer = [a, b, c, comp(c), comp(b), comp(a)]
sixmer = np.empty((N, N_6MERS, 6), dtype=np.uint8)
sixmer[..., 0] = abc[..., 0]
sixmer[..., 1] = abc[..., 1]
sixmer[..., 2] = abc[..., 2]
sixmer[..., 3] = 3 - abc[..., 2]
sixmer[..., 4] = 3 - abc[..., 1]
sixmer[..., 5] = 3 - abc[..., 0]
tail_palin = sixmer.reshape(N, N_6MERS * 6)
tail_pad = rng.integers(0, 4, size=(N, PAD), dtype=np.uint8)
tail = np.concatenate([tail_palin, tail_pad], axis=1)
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
