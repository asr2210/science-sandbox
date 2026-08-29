"""Per-sequence varied composition. 50K sequences, each with random
GC fraction in [0,1]. Tests if oracle is composition-sensitive."""
import os, random
random.seed(7)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for i in range(50000):
        gc = i / 49999
        seq_chars = []
        for _ in range(200):
            if random.random() < gc:
                seq_chars.append(random.choice("12"))
            else:
                seq_chars.append(random.choice("03"))
        f.write("".join(seq_chars) + "\n")
print("wrote 50000 sequences with varying GC fractions 0..1")
