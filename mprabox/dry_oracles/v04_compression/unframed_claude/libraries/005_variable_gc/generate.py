"""Experiment 005: Per-sequence variable GC.

Each of 50k sequences gets a target GC fraction sampled uniformly in [0.2, 0.8];
the sequence is then i.i.d. random with that GC. Library has wide between-
sequence GC variance, while individual sequences are uniform random.

Probes whether library-level variance (theory A/B) or genome-like composition
(theory C) drives the score.
"""
import numpy as np
import os

N_SEQ = 50000
LEN = 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(20260606)
gcs = rng.uniform(0.2, 0.8, size=N_SEQ)

seqs = []
for gc in gcs:
    pA = pT = (1 - gc) / 2
    pC = pG = gc / 2
    idx = rng.choice(4, size=LEN, p=[pA, pC, pG, pT])
    seqs.append("".join(ALPHABET[idx]))

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_SEQ} variable-GC sequences to {out_path}")
print(f"  GC range: {gcs.min():.3f} – {gcs.max():.3f}")
