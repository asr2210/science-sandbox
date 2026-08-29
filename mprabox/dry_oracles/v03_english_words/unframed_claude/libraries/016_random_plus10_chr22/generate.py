"""90% random uniform + 10% chr22 fragments.
Test: how small a chr22 fraction is needed to lift SKNSH meaningfully,
and how much it costs K562/HepG2?
"""
import numpy as np
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

N = 50000
N_CHR = 5000
N_RAND = N - N_CHR
L = 200
rng = np.random.default_rng(16)
ALPH = np.array(list("ACGT"))

rand = ALPH[rng.integers(0, 4, size=(N_RAND, L))]
seqs_rand = ["".join(r) for r in rand]

parts = []
with open(FA) as f:
    for line in f:
        if not line.startswith(">"):
            parts.append(line.strip().upper())
chrom = "".join(parts)
runs = [m.group() for m in re.finditer(r"[ACGT]{200,}", chrom)]
weights = np.array([max(0, len(r) - L + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()
seqs_chr = []
for _ in range(N_CHR):
    r = runs[int(rng.choice(len(runs), p=weights))]
    s = int(rng.integers(0, len(r) - L + 1))
    seqs_chr.append(r[s:s + L])

all_seqs = seqs_rand + seqs_chr
rng.shuffle(all_seqs)

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"Wrote {N} sequences (45k random + 5k chr22)")
