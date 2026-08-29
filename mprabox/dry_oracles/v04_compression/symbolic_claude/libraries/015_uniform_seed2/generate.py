"""Same as 001 but seed=2. Second variance datapoint to triangulate ceiling."""
import os, random
random.seed(2)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(50000):
        f.write("".join(random.choice("0123") for _ in range(200)) + "\n")
print("wrote 50000 uniform random (seed=2)")
