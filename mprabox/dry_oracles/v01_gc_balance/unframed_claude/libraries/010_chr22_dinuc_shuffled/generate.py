"""Experiment 010: chr22 sequences with per-sequence shuffle.
Per-sequence mononucleotide shuffle: preserves per-sequence GC content,
destroys all higher-order structure (motifs, dinucleotide patterns).

If shuffled ~ same as 005 (0.678): motifs don't matter, only mononuc composition.
If shuffled << 005: motifs/dinucleotides matter.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
SRC = os.path.join(os.path.dirname(__file__), "..", "005_real_human_chr22", "sequences_0.txt")

with open(SRC) as f:
    src_seqs = [ln.strip() for ln in f if ln.strip()]
print(f"Loaded {len(src_seqs)} source sequences")

rng = np.random.default_rng(52)
out = []
for s in src_seqs:
    arr = np.frombuffer(s.encode(), dtype="|S1").copy()
    rng.shuffle(arr)
    out.append(arr.tobytes().decode())
print(f"Shuffled {len(out)}")
with open(OUT, "w") as f:
    f.write("\n".join(out) + "\n")
print("Wrote.")
