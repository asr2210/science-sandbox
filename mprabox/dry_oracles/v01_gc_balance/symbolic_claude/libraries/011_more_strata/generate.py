"""
Experiment 011: more compositional strata + anchors.

- 4 letter anchors × 1250 = 5000 (10% anchor weight)
- 6 random strata × 7500 = 45000
  S1: uniform random
  S2: GC-rich (weights [1,4,4,1])
  S3: AT-rich (weights [4,1,1,4])
  S4: very GC-rich (weights [1,9,9,1])
  S5: very AT-rich (weights [9,1,1,9])
  S6: no-homopolymer
"""
import os, random

random.seed(11)
L = 200
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

def no_hp(maxrun=4):
    while True:
        s = "".join(random.choices(ALPHABET, k=L))
        run = 1; mx = 1
        for i in range(1, L):
            if s[i] == s[i-1]:
                run += 1
                if run > mx: mx = run
            else:
                run = 1
        if mx <= maxrun:
            return s

lines = []
# 4 letter anchors × 1250 = 5000
for ch in "0123":
    lines += [ch * L] * 1250

# 6 strata × 7500
configs = [
    ([1,1,1,1], "uniform"),
    ([1,4,4,1], "GC-rich"),
    ([4,1,1,4], "AT-rich"),
    ([1,9,9,1], "very-GC-rich"),
    ([9,1,1,9], "very-AT-rich"),
]
for w, name in configs:
    for _ in range(7500):
        lines.append("".join(random.choices(ALPHABET, weights=w, k=L)))
# 6th: no-homopolymer
for _ in range(7500):
    lines.append(no_hp())

assert len(lines) == 50000

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} seqs")
