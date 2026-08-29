"""Experiment 003: Compositional extremes (4-way bias mix).

50,000 strings total: 12,500 strings strongly biased toward each
of the 4 characters (80% target char, 20% uniform over others).
Maximizes variance of per-character fraction across the library.

If correlation depends on compositional features, this should push
score significantly above the uniform random baseline.
"""
import os
import random

random.seed(2)

N_PER_CLASS = 12_500
L = 200
ALPHABET = "0123"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for target in ALPHABET:
        others = [c for c in ALPHABET if c != target]
        for _ in range(N_PER_CLASS):
            chars = []
            for _ in range(L):
                if random.random() < 0.8:
                    chars.append(target)
                else:
                    chars.append(random.choice(others))
            f.write("".join(chars) + "\n")

print(f"Wrote {4 * N_PER_CLASS} strings to {out_path}")
