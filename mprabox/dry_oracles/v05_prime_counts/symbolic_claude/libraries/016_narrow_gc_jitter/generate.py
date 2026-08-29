"""Per-sequence GC ~ N(0.5, 0.05), then sample positions i.i.d.
Tests slightly elevated per-seq composition variance (between baseline
~0.03 binomial sd and exp 008's broad uniform sd ~0.23)."""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        gc = max(0.05, min(0.95, random.gauss(0.5, 0.05)))
        # split GC and AT halves equally
        a, t = (1 - gc) / 2, (1 - gc) / 2
        c, g = gc / 2, gc / 2
        w = [a, c, g, t]
        f.write("".join(random.choices(ALPHA, weights=w, k=L)) + "\n")
print(f"Wrote {N} narrow-jittered-GC sequences")
