"""Random sequences with high AT content (60% A/T = chars 0,3).
Tests symmetric counterpart to exp 005."""
import random, os
random.seed(42)
N, L = 50_000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
weights = [0.30, 0.20, 0.20, 0.30]  # A C G T
alpha = "0123"
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choices(alpha, weights=weights, k=L)) + "\n")
print(f"Wrote {N} AT-biased sequences (60% AT)")
