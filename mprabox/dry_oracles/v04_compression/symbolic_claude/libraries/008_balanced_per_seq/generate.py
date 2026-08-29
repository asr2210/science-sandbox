"""Each sequence has exactly 50 of each character, randomly shuffled.
Tests per-sequence composition balance vs iid uniform."""
import os, random
random.seed(42)
chars = list("0" * 50 + "1" * 50 + "2" * 50 + "3" * 50)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        random.shuffle(chars)
        f.write("".join(chars) + "\n")
print("wrote 50000 per-seq-balanced sequences (exactly 50 of each char)")
