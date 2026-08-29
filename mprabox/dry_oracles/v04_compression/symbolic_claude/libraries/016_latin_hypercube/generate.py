"""Latin Hypercube: exact positional balance.
Each of 200 positions contains exactly 12500 of each character.
Per-sequence composition remains approximately binomial (similar to iid).

This eliminates positional sampling noise while keeping iid-like sequence
properties.
"""
import os, random
random.seed(42)

N = 50000
L = 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Build column-by-column: each column is a balanced shuffle.
# Then transpose to get N sequences.
columns = []
for p in range(L):
    col = [c for c in "0123" for _ in range(N // 4)]
    random.shuffle(col)
    columns.append(col)

with open(out_path, "w") as f:
    for i in range(N):
        f.write("".join(columns[p][i] for p in range(L)) + "\n")
print("wrote 50000 Latin Hypercube sequences (exact positional balance)")
