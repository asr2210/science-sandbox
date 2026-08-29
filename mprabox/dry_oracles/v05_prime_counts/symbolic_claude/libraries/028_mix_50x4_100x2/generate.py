"""Mix: 25K sequences as 50bp x 4 tandem + 25K as 100bp x 2 tandem.
Tests whether two-strategy mix can outperform either alone."""
import random, os
random.seed(43)
N_HALF = 25_000
L = 200
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    # 50 x 4
    for _ in range(N_HALF):
        unit = "".join(random.choice(ALPHA) for _ in range(50))
        f.write(unit * 4 + "\n")
    # 100 x 2
    for _ in range(N_HALF):
        unit = "".join(random.choice(ALPHA) for _ in range(100))
        f.write(unit * 2 + "\n")
print(f"Wrote {2 * N_HALF} mixed-tandem sequences")
