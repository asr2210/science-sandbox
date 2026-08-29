"""50K copies of periodic tile '0123'*50. Pure deterministic structure."""
import os
seq = "0123" * 50
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write(seq + "\n")
print("wrote 50000 copies of '0123'*50")
