"""001 — Random uniform baseline.
50,000 sequences of length 200, i.i.d. uniform over {0,1,2,3}.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200

rng = np.random.default_rng(42)
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

with open(OUT, "w") as f:
    for row in arr:
        f.write(row.tobytes().translate(bytes.maketrans(b"\x00\x01\x02\x03", b"0123")).decode("ascii"))
        f.write("\n")
print(f"wrote {N} sequences of length {L}")
