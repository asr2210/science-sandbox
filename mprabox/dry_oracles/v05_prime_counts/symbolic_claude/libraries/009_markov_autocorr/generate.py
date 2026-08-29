"""1st-order Markov chain with autocorrelation (P(same)=0.4, P(other)=0.2 each).
Tests whether positional autocorrelation helps."""
import random, os
random.seed(42)
N, L = 50_000, 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ALPHA = "0123"

def next_base(prev):
    r = random.random()
    if r < 0.4:
        return prev
    # uniform over the other 3
    r2 = random.random()
    others = [b for b in ALPHA if b != prev]
    return others[int(r2 * 3)]

with open(out_path, "w") as f:
    for _ in range(N):
        s = [random.choice(ALPHA)]
        for _ in range(L - 1):
            s.append(next_base(s[-1]))
        f.write("".join(s) + "\n")
print(f"Wrote {N} Markov sequences (P(same)=0.4)")
