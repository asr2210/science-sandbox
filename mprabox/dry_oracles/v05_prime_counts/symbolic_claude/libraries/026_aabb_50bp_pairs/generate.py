"""Each sequence = A + A + B + B where A, B are independent random 50bp units.
Tests two-tandem structure vs single 50bp x 4 tandem."""
import random, os
random.seed(43)
N, L = 50_000, 200
UNIT = 50
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        a = "".join(random.choice(ALPHA) for _ in range(UNIT))
        b = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(a + a + b + b + "\n")
print(f"Wrote {N} AABB sequences (50bp units)")
