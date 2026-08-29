"""Scaled palindrome: palindromic at both length 200 (whole sequence)
AND length 100 (each half is independently palindromic).

Construction: 50 random + revcomp(50) + 50 random + revcomp(50).
Equivalently: positions 0-49 free, 50-99 = revcomp(0-49), 100-149 free,
150-199 = revcomp(100-149).

Wait — actually a true scaled palindrome would have positions 0-99
equal to positions 100-199 (direct repeat), each being palindromic.
Implementing as: A(50) + RC(A)(50) + B(50) + RC(B)(50)? No, that
isn't a length-200 palindrome.

Use the derivation in notebook: free A=[0..49], rest determined as
A + RC(A) + A + RC(A). Each half is a palindrome, AND the whole is
a length-200 palindrome under RC.
"""
import numpy as np
import os

rng = np.random.default_rng(1818)
N, L = 50000, 200
A_LEN = 50

A = rng.integers(0, 4, size=(N, A_LEN), dtype=np.uint8)
RC_A = (3 - A).astype(np.uint8)[:, ::-1]
arr = np.concatenate([A, RC_A, A, RC_A], axis=1)
assert arr.shape == (N, L)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(str(x) for x in row.tolist()))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
