"""Random sequences over only {1,2}. Tests biased composition."""
import os, random
random.seed(42)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write("".join(random.choice("12") for _ in range(200)) + "\n")
print("wrote 50000 random sequences over {1,2}")
