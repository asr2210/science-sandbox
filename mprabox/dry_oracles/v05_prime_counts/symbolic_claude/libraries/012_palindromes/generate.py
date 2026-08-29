"""Palindromic sequences: first 100bp random, last 100bp = reverse complement.
With {0=A, 1=C, 2=G, 3=T}: complement is 0<->3, 1<->2.
Tests strand-symmetry hypothesis."""
import random, os
random.seed(42)
N, L = 50_000, 200
HALF = L // 2
ALPHA = "0123"
COMP = {"0": "3", "1": "2", "2": "1", "3": "0"}
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        first = [random.choice(ALPHA) for _ in range(HALF)]
        second = [COMP[b] for b in first[::-1]]
        f.write("".join(first) + "".join(second) + "\n")
print(f"Wrote {N} palindromic sequences")
