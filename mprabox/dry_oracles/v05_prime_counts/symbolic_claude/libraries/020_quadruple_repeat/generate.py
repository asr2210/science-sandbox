"""Each sequence: 50bp random repeated 4 times to fill 200bp.
Pushes self-similarity probe further than exp 019."""
import random, os
random.seed(42)
N, L = 50_000, 200
UNIT = 50
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(unit * (L // UNIT) + "\n")
print(f"Wrote {N} quadruple-repeat sequences (50bp x 4)")
