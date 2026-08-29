"""Each sequence: first 100bp random, second 100bp = same as first.
Tests whether scoring rewards self-similarity / first-half = second-half."""
import random, os
random.seed(42)
N, L = 50_000, 200
HALF = L // 2
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        half = "".join(random.choice(ALPHA) for _ in range(HALF))
        f.write(half + half + "\n")
print(f"Wrote {N} repeated-halves sequences")
