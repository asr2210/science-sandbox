import numpy as np

rng = np.random.default_rng(42)
arr = rng.integers(0, 4, size=(50000, 200), dtype=np.int8)
with open("libraries/001_random_baseline/sequences_0.txt", "w") as f:
    for row in arr:
        f.write("".join(map(str, row.tolist())) + "\n")
