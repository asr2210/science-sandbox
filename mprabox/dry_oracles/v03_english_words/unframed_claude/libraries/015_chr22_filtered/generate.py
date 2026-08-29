"""chr22 fragments filtered to remove pathological regions:
- GC content in [0.40, 0.60]
- No single-base run > 8
- Reject if any 6-mer appears > 5 times (kills tandem repeats / low complexity)
Test: does cleaning chr22 preserve SKNSH boost while recovering K562/HepG2?
"""
import numpy as np
from pathlib import Path
import re
from collections import Counter

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

N, L = 50000, 200
rng = np.random.default_rng(15)

parts = []
with open(FA) as f:
    for line in f:
        if not line.startswith(">"):
            parts.append(line.strip().upper())
chrom = "".join(parts)
runs = [m.group() for m in re.finditer(r"[ACGT]{200,}", chrom)]
weights = np.array([max(0, len(r) - L + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()

def keep(frag: str) -> bool:
    gc = (frag.count("G") + frag.count("C")) / len(frag)
    if not (0.40 <= gc <= 0.60):
        return False
    if re.search(r"([ACGT])\1{8,}", frag):
        return False
    kmer_counts = Counter(frag[i:i+6] for i in range(len(frag) - 5))
    if max(kmer_counts.values()) > 5:
        return False
    return True

seqs = []
attempts = 0
while len(seqs) < N:
    attempts += 1
    r = runs[int(rng.choice(len(runs), p=weights))]
    s = int(rng.integers(0, len(r) - L + 1))
    frag = r[s:s + L]
    if keep(frag):
        seqs.append(frag)

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} filtered chr22 fragments (kept {N/attempts*100:.1f}% of draws)")
