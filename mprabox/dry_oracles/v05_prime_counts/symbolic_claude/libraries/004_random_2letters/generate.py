"""Random over only {0,1} alphabet. Tests whether using a 2-letter
subset of the alphabet impacts score."""
import random, os
random.seed(42)
N, L = 50_000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choice("01") for _ in range(L)) + "\n")
print(f"Wrote {N} 2-letter sequences")
