"""Per-sequence shuffle of chr22 fragments.
Preserves single-base composition (per-sequence GC, AT) but destroys
all motifs, repeats, and dinucleotide patterns.
Diagnostic: is the SKNSH boost from chr22 due to composition (preserved)
or due to structure (destroyed)?
"""
import numpy as np
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

N, L = 50000, 200
rng = np.random.default_rng(12)

parts = []
with open(FA) as f:
    for line in f:
        if not line.startswith(">"):
            parts.append(line.strip().upper())
chrom = "".join(parts)
runs = [m.group() for m in re.finditer(r"[ACGT]{200,}", chrom)]
weights = np.array([max(0, len(r) - L + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()

seqs = []
for _ in range(N):
    r = runs[int(rng.choice(len(runs), p=weights))]
    s = int(rng.integers(0, len(r) - L + 1))
    frag = list(r[s:s + L])
    rng.shuffle(frag)
    seqs.append("".join(frag))

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} per-seq shuffled chr22 fragments")
