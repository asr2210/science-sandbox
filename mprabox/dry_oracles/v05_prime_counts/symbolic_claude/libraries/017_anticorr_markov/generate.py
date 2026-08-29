"""Anti-correlated Markov: P(same)=0 (every position differs from previous).
Doubly stochastic so marginal is uniform. Tests negative-autocorrelation."""
import random, os
random.seed(42)
N, L = 50_000, 200
ALPHA = "0123"

def next_base(prev):
    return random.choice([b for b in ALPHA if b != prev])

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        s = [random.choice(ALPHA)]
        for _ in range(L - 1):
            s.append(next_base(s[-1]))
        f.write("".join(s) + "\n")
print(f"Wrote {N} anti-correlated Markov sequences")
