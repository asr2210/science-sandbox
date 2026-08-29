"""Random sequences with high GC content (60% G/C). Tests whether
biasing toward G/C improves scores.

Mapping convention: {0=A, 1=C, 2=G, 3=T}. GC = chars {1,2}.
This gives P(0)=0.20, P(1)=0.30, P(2)=0.30, P(3)=0.20."""
import random, os
random.seed(42)
N, L = 50_000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
weights = [0.20, 0.30, 0.30, 0.20]  # A C G T
alpha = "0123"
with open(out_path, "w") as f:
    for _ in range(N):
        f.write("".join(random.choices(alpha, weights=weights, k=L)) + "\n")
print(f"Wrote {N} GC-biased sequences (60% GC)")
