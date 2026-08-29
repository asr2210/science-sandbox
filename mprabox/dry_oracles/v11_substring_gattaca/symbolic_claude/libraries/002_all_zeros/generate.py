"""All-zeros monoculture: tests if single-character sequences are penalized."""
import os
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(OUT, "w") as f:
    for _ in range(50000):
        f.write("0" * 200 + "\n")
print("wrote 50000 'all 0' sequences")
