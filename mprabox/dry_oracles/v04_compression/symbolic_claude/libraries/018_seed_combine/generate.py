"""Combine: 25K from Python seed=1 and 25K from Python seed=2.
Tests whether mixing two good seeds gives a meta-improvement."""
import os, random

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
lines = []
for seed in (1, 2):
    random.seed(seed)
    for _ in range(25000):
        lines.append("".join(random.choice("0123") for _ in range(200)))
# shuffle interleaved so the eval doesn't see them grouped
random.seed(99)
random.shuffle(lines)
with open(out_path, "w") as f:
    for s in lines:
        f.write(s + "\n")
print("wrote 25K seed=1 + 25K seed=2 (shuffled)")
