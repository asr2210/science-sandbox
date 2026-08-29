"""40bp random unit repeated 5 times. Interpolates between 25bpx8 and 50bpx4."""
import random, os
random.seed(42)
N, L = 50_000, 200
UNIT = 40
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(unit * (L // UNIT) + "\n")
print(f"Wrote {N} 40bp-x5 sequences")
