"""20bp random unit repeated 10 times = 200bp.
Tests very small tandem repeat unit (still divisor of 200)."""
import random, os
random.seed(42)
N, L = 50_000, 200
UNIT = 20
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(unit * (L // UNIT) + "\n")
print(f"Wrote {N} 20bp-x10 sequences")
