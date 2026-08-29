"""Experiment 002: 50K identical constant '0'*200 sequences.

Probes two things simultaneously:
- Whether duplicate sequences are penalized (vs unique random in exp 001)
- Score of a pure all-nucleotide-0 string
"""
import os

N_SEQS = 50_000
LEN = 200
seq = "0" * LEN

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N_SEQS):
        f.write(seq + "\n")
print(f"Wrote {N_SEQS} identical sequences to {out_path}")
