"""Markov chain with CpG depletion. Doubly-stochastic transition matrix:
marginal stays uniform (25% each), but P(G|C) = 0.05 (suppressed CpG).
With {0=A,1=C,2=G,3=T}: transition (1,2) is suppressed."""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"

# rows = prev, cols = next, with P(G|C) = 0.05 (suppressed)
# Doubly stochastic. Recomputed by hand.
P = {
    "0": {"0": 0.25, "1": 0.25, "2": 0.30, "3": 0.20},
    "1": {"0": 0.30, "1": 0.30, "2": 0.05, "3": 0.35},
    "2": {"0": 0.25, "1": 0.25, "2": 0.30, "3": 0.20},
    "3": {"0": 0.20, "1": 0.20, "2": 0.35, "3": 0.25},
}
# Quick sanity check
for prev, row in P.items():
    assert abs(sum(row.values()) - 1.0) < 1e-6

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = [random.choice(ALPHA)]
        for _ in range(L - 1):
            row = P[s[-1]]
            s.append(random.choices(ALPHA, weights=[row[b] for b in ALPHA], k=1)[0])
        f.write("".join(s) + "\n")
print(f"Wrote {N} CpG-depleted Markov sequences (uniform marginal)")
