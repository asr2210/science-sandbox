"""
Experiment 010: 4 diverse random strata, NO anchors.

Tests: do anchors actually help, or was it the diverse random strata
doing the work in exp 009?

Strata: uniform random, GC-rich, AT-rich, no-homopolymer.
12500 unique seqs each.
"""
import os, random

random.seed(10)
L = 200
ALPHABET = "0123"
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

def no_homopolymer_seq():
    while True:
        s = "".join(random.choices(ALPHABET, k=L))
        max_run = 1; run = 1
        for i in range(1, L):
            if s[i] == s[i-1]:
                run += 1; max_run = max(max_run, run)
            else:
                run = 1
        if max_run < 5:
            return s

lines = []
# uniform
for _ in range(12500):
    lines.append("".join(random.choices(ALPHABET, k=L)))
# GC-rich
for _ in range(12500):
    lines.append("".join(random.choices(ALPHABET, weights=[1,4,4,1], k=L)))
# AT-rich
for _ in range(12500):
    lines.append("".join(random.choices(ALPHABET, weights=[4,1,1,4], k=L)))
# no-homopolymer
for _ in range(12500):
    lines.append(no_homopolymer_seq())

assert len(lines) == 50000

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} seqs (4 diverse random strata, no anchors)")
