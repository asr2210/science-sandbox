"""Re-purposed: 1000 unique random sequences × 50 copies each = 50K total.
Tests if reduced diversity (1K unique vs 50K unique) hurts score."""
import os, random
random.seed(123)
uniques = ["".join(random.choice("0123") for _ in range(200)) for _ in range(1000)]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in uniques:
        for _ in range(50):
            f.write(s + "\n")
print("wrote 1000 uniques x 50 copies = 50000 sequences")
