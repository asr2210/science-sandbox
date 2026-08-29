"""50K copies of '0'*200. Maximum degenerate."""
import os
seq = "0" * 200
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write(seq + "\n")
print("wrote 50000 copies of '0'*200")
