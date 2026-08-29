"""Mix first 25k of seed=42 and first 25k of seed=1 (the two top seeds).

Two top seeds for the [43,57] uniform-tuples + shuffle recipe were:
  - seed=42 (009): 0.8820
  - seed=1  (022): 0.8815

Concatenating 25k from each tests whether averaging two lucky draws
keeps the quality (suggesting it's a stable equilibrium) or breaks it
(suggesting per-draw idiosyncrasy is doing the work).
"""
import os

base = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

src_a = os.path.join(base, "009_wider_constrained", "sequences_0.txt")
src_b = os.path.join(base, "022_asymmetric_42_57", "sequences_0.txt")

with open(OUT, "w") as f_out:
    with open(src_a) as f_a:
        for i, line in enumerate(f_a):
            if i >= 25000:
                break
            f_out.write(line)
    with open(src_b) as f_b:
        for i, line in enumerate(f_b):
            if i >= 25000:
                break
            f_out.write(line)

print(f"wrote 50000 sequences (mix of seed=42 first 25k + seed=1 first 25k)")
