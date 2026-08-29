"""Symmetric doubly-stochastic Markov: uniform stationary, mild
self-preference (diag = 0.4, off-diag = 0.2). Tests if any
1st-order correlation hurts even when composition is preserved.
"""
import os, random
random.seed(42)
chars = "0123"
diag = 0.4
off = 0.2
P = {c: [diag if c2 == c else off for c2 in chars] for c in chars}
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        s = [random.choice(chars)]
        for _ in range(199):
            s.append(random.choices(chars, weights=P[s[-1]])[0])
        f.write("".join(s) + "\n")
print("wrote 50000 symmetric Markov sequences (uniform stationary, diag=0.4)")
