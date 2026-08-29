#!/usr/bin/env python3
"""Random + 10-char dinucleotide repeat inserted at random position.

5 groups of 10000:
- pure random (control)
- random + "(01)*5" at random pos
- random + "(12)*5"
- random + "(23)*5"
- random + "(03)*5"

Each insertion is 10 chars, 5 of each pair (locally balanced for that pair).
Tests if simple repeat motifs unlock condition_c.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
GROUP_SIZE = 10000
ALPHA = "0123"

motifs = [None, "01" * 5, "12" * 5, "23" * 5, "03" * 5]

def rand_seq(length: int) -> str:
    return "".join(random.choice(ALPHA) for _ in range(length))

def insert_motif(seq: str, motif: str) -> str:
    if motif is None:
        return seq
    pos = random.randint(0, len(seq) - len(motif))
    return seq[:pos] + motif + seq[pos + len(motif):]

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for m in motifs:
        for _ in range(GROUP_SIZE):
            seq = rand_seq(L)
            seq = insert_motif(seq, m)
            f.write(seq + "\n")

print(f"Wrote {N} sequences with 5 motif groups to {out_path}")
