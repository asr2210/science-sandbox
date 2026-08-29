"""Mix: 25k random uniform + 25k chr22 fragments.
Random is good for K562/HepG2; real DNA is good for SKNSH.
See if mixing preserves the gains in each direction.
"""
import numpy as np
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

N_HALF = 25000
L = 200
rng = np.random.default_rng(11)
ALPH = np.array(list("ACGT"))

# half A: random uniform
randA = ALPH[rng.integers(0, 4, size=(N_HALF, L))]
seqs_A = ["".join(r) for r in randA]

# half B: real chr22
parts = []
with open(FA) as f:
    for line in f:
        if not line.startswith(">"):
            parts.append(line.strip().upper())
chrom = "".join(parts)
runs = [m.group() for m in re.finditer(r"[ACGT]{200,}", chrom)]
weights = np.array([max(0, len(r) - L + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()
seqs_B = []
for _ in range(N_HALF):
    r = runs[int(rng.choice(len(runs), p=weights))]
    s = int(rng.integers(0, len(r) - L + 1))
    seqs_B.append(r[s:s + L])

all_seqs = seqs_A + seqs_B
rng.shuffle(all_seqs)

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"Wrote {len(all_seqs)} sequences (25k random + 25k chr22)")
