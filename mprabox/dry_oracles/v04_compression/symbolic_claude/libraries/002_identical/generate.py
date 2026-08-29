"""50K copies of one random sequence. Tests if score depends on
library diversity."""
import os, random
random.seed(42)
seq = "".join(random.choice("0123") for _ in range(200))
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write(seq + "\n")
print(f"wrote 50000 copies of: {seq[:40]}...")
