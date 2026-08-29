"""Try numpy's PCG64 RNG for comparison with Python's Mersenne Twister.
Same distribution (iid uniform) but different bit patterns. Tests if
the specific seed-stream matters or it's all in-noise iid."""
import os
import numpy as np
rng = np.random.default_rng(42)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
arr = rng.integers(0, 4, size=(50000, 200), dtype=np.int8)
with open(out_path, "w") as f:
    for row in arr:
        f.write("".join(map(str, row.tolist())) + "\n")
print("wrote 50000 iid uniform with numpy PCG64 seed=42")
