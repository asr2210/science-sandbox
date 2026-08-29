"""
Experiment 009: anchor-fraction sweep. 20% anchors, 80% diverse random.

Library:
- 4 letter constants × 2500 = 10000 (20% anchor weight)
- 4 random strata × 10000 each = 40000 (80% diverse random)
   uniform random, GC-rich, AT-rich, GC-balanced-with-no-homopolymers

Hypothesis: less anchor weight + more diverse random might raise r.
Comparison points:
- exp 003 random only: 0.5299 (eval_01)
- exp 005 with 62.5% anchor weight: 0.5627 (eval_01) BEST
- exp 009 with 20% anchor weight: ?

If > 0.5627: less anchor is better; push lower.
If < 0.5627: anchors at ~60% are sweet spot or higher needed.
"""
import os, random

random.seed(9)
L = 200
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

lines = []

# 4 letter anchors × 2500 each
for ch in "0123":
    lines += [ch * L] * 2500

# Stratum 1: uniform random × 10000
for _ in range(10000):
    lines.append("".join(random.choices(ALPHABET, k=L)))

# Stratum 2: GC-rich random × 10000
for _ in range(10000):
    lines.append("".join(random.choices(ALPHABET, weights=[1,4,4,1], k=L)))

# Stratum 3: AT-rich random × 10000
for _ in range(10000):
    lines.append("".join(random.choices(ALPHABET, weights=[4,1,1,4], k=L)))

# Stratum 4: balanced random with no long homopolymers (resample if found 5+ same)
def no_homopolymer_seq():
    while True:
        s = "".join(random.choices(ALPHABET, k=L))
        # check max run-length
        max_run = 1
        run = 1
        for i in range(1, L):
            if s[i] == s[i-1]:
                run += 1
                if run > max_run:
                    max_run = run
            else:
                run = 1
        if max_run < 5:
            return s

for _ in range(10000):
    lines.append(no_homopolymer_seq())

assert len(lines) == 50000

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} seqs (20% anchor weight, 80% diverse random)")
