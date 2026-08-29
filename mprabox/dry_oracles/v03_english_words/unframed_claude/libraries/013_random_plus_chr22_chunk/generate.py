"""Each sequence = 100bp random uniform + 100bp chr22 fragment, concatenated.
Tests if intra-sequence chimera preserves K562/HepG2 (from random half)
while still triggering the SKNSH boost (from chr22 half).
"""
import numpy as np
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

N = 50000
L_RAND = 100
L_CHR = 100
rng = np.random.default_rng(13)
ALPH = np.array(list("ACGT"))

parts = []
with open(FA) as f:
    for line in f:
        if not line.startswith(">"):
            parts.append(line.strip().upper())
chrom = "".join(parts)
runs = [m.group() for m in re.finditer(r"[ACGT]{200,}", chrom)]
weights = np.array([max(0, len(r) - L_CHR + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()

seqs = []
for _ in range(N):
    rand = "".join(ALPH[rng.integers(0, 4, L_RAND)])
    r = runs[int(rng.choice(len(runs), p=weights))]
    s = int(rng.integers(0, len(r) - L_CHR + 1))
    chr_frag = r[s:s + L_CHR]
    # randomize which half is first
    if rng.random() < 0.5:
        seqs.append(rand + chr_frag)
    else:
        seqs.append(chr_frag + rand)

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} chimera sequences (100bp random + 100bp chr22)")
