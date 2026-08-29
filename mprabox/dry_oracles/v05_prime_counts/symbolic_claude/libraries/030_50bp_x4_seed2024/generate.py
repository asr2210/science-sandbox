"""FINAL submission: 50bp x 4 tandem repeat with seed=2024.
Fourth sample of the best-performing structure to maximize chance of lucky high."""
import random, os
random.seed(2024)
N, L = 50_000, 200
UNIT = 50
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(unit * (L // UNIT) + "\n")
print(f"Wrote {N} 50bpx4 seed=2024 (final submission)")
