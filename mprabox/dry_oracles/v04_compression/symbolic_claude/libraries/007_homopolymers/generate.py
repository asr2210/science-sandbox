"""Mixed library: 12,500 of '0'*200, '1'*200, '2'*200, '3'*200.
Each sequence is one character; library has 4 unique seqs."""
import os
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for c in "0123":
        s = c * 200 + "\n"
        for _ in range(12500):
            f.write(s)
print("wrote 12,500 copies each of '0'*200, '1'*200, '2'*200, '3'*200")
