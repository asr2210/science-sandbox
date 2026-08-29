"""Experiment 017: random 200bp slices from 4 gene-dense chromosomes (17, 19, 20, 22).
~12.5k each. These are the most gene-dense human chromosomes."""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FASTA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hg38.fa")
L = 200
TARGETS = ["chr17", "chr19", "chr20", "chr22"]
PER = 12_500

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
rng = np.random.default_rng(120)
seqs = []
for chrom in TARGETS:
    cl = len(fa[chrom])
    print(f"{chrom}: {cl}")
    count = 0
    attempts = 0
    while count < PER and attempts < PER * 5:
        attempts += 1
        p = rng.integers(0, cl - L)
        s = str(fa[chrom][p:p+L])
        if len(s) == L and "N" not in s:
            seqs.append(s)
            count += 1
    print(f"  got {count}")
print(f"Total: {len(seqs)}")
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
