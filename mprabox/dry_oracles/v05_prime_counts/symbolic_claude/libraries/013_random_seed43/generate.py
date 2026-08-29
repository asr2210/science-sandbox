"""Random uniform with seed=43 (reproduce 001 with different seed).
Measures noise floor for identical-distribution libraries."""
import random, os
random.seed(43)
N, L = 50_000, 200
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choice(ALPHA) for _ in range(L)) + "\n")
print(f"Wrote {N} sequences seed=43")
