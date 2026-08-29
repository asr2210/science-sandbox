"""Random uniform but reject sequences whose per-base count is outside [45, 55].
Tests whether tighter per-sequence composition (reduced binomial tail variance)
improves or worsens score."""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"
LO, HI = 45, 55
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

def ok(s):
    return all(LO <= s.count(c) <= HI for c in ALPHA)

written = 0
with open(out_path, "w") as f:
    while written < N:
        s = "".join(random.choice(ALPHA) for _ in range(L))
        if ok(s):
            f.write(s + "\n")
            written += 1
print(f"Wrote {N} tightly-balanced sequences")
