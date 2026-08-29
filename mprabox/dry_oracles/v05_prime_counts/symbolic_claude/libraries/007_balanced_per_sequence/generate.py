"""Each sequence has exactly 50 of each base (perfectly balanced),
shuffled randomly. Tests whether per-sequence composition uniformity
helps vs. independent per-position random."""
import random, os
random.seed(42)
N, L = 50_000, 200
base = "0" * 50 + "1" * 50 + "2" * 50 + "3" * 50
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        chars = list(base)
        random.shuffle(chars)
        f.write("".join(chars) + "\n")
print(f"Wrote {N} balanced sequences")
