"""Random 50k subset of Gosai et al 2024 Malinois MPRA dataset.

Hypothesis: prepare.py oracles were trained on (or correlate with) the
Malinois MPRA dataset. Submitting real biological 200bp MPRA sequences
should drastically outperform random sequences for K562/HepG2/SKNSH.
"""
import os, random

random.seed(5)
N_SEQS, LENGTH = 50000, 200

DATA = "/data/users/arao/.private/MPRAgent_adversarial/runs/v02/unknown_claude/data/malinois_mpra.txt"

seqs = []
with open(DATA) as f:
    header = f.readline()
    for line in f:
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 12:
            continue
        s = cols[11].upper()
        if len(s) == LENGTH and all(c in "ACGT" for c in s):
            seqs.append(s)

print(f"Found {len(seqs)} candidate 200bp ACGT sequences")
random.shuffle(seqs)
chosen = seqs[:N_SEQS]
assert len(chosen) == N_SEQS

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    for s in chosen:
        f.write(s + "\n")
print(f"Wrote {N_SEQS} sequences to {out}")
