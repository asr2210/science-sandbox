"""Experiment 13: Direct sampling from the Malinois MPRA training set.

Source: Tewhey/Gosai/Sabeti Lab — 776K 200bp sequences measured in K562,
HepG2, SKNSH MPRA assays (Table_S2__MPRA_dataset.txt).

Hypothesis: these are the EXACT sequences the ground-truth and eval models
were trained on. The two model predictions on training-distribution sequences
should agree the most → highest Pearson r.

Pick 50K uniform-random rows, filter for valid 200bp ACGT sequences.
"""

import numpy as np
import csv
from pathlib import Path
import re

rng = np.random.default_rng(seed=13)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"
src = DATA / "mpra_dataset.txt"

print("Reading MPRA dataset...")
sequences = []
with open(src) as f:
    header = f.readline().rstrip("\n").split("\t")
    seq_idx = header.index("sequence")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= seq_idx:
            continue
        s = parts[seq_idx].upper()
        if len(s) == L and set(s) <= set("ACGT"):
            sequences.append(s)
print(f"Loaded {len(sequences):,} valid 200bp ACGT sequences")

# Sample N uniformly without replacement
if len(sequences) >= N:
    idx = rng.choice(len(sequences), size=N, replace=False)
    out = [sequences[i] for i in idx]
else:
    out = sequences[:]
    # If not enough, sample with replacement to pad
    pad = N - len(out)
    idx = rng.choice(len(sequences), size=pad, replace=True)
    out.extend(sequences[i] for i in idx)

assert len(out) == N
rng.shuffle(out)
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")

arr = np.array([[ord(b) for b in s] for s in out[:10000]], dtype=np.int8)
gc = ((arr == ord('C')) | (arr == ord('G'))).mean(axis=1)
print(f"GC (10k sample): mean={gc.mean():.3f}, std={gc.std():.3f}, "
      f"range=[{gc.min():.3f}, {gc.max():.3f}]")
print(f"Wrote {len(out)} MPRA training sequences")
