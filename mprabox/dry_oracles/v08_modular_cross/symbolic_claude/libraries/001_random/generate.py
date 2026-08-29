import numpy as np
import os

np.random.seed(42)
N = 50000
L = 200
arr = np.random.randint(0, 4, size=(N, L), dtype=np.uint8)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(N):
        f.write("".join(str(x) for x in arr[i]) + "\n")
print(f"wrote {N} sequences to {out_path}")
