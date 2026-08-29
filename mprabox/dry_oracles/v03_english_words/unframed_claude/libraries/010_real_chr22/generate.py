"""Real human DNA fragments from chr22 (GRCh38).
Test in-distribution hypothesis: does the predictor score real DNA
higher than uniform random?
"""
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
FA = HERE.parent.parent / "data" / "chr22.fa"

# Read chr22 as one big string, strip header and newlines, uppercase.
parts = []
with open(FA) as f:
    for line in f:
        if line.startswith(">"):
            continue
        parts.append(line.strip().upper())
chrom = "".join(parts)
print(f"chr22 length: {len(chrom):,}")

# Mask out unsequenced N regions; keep only contiguous ACGT runs ≥ 200.
import re
runs = [m for m in re.finditer(r"[ACGT]{200,}", chrom)]
total_acgt = sum(len(r.group()) for r in runs)
print(f"contiguous ACGT runs (≥200): {len(runs)}, total bases: {total_acgt:,}")

# Sample 50k random 200bp windows from these runs.
N, L = 50000, 200
rng = np.random.default_rng(10)
# pick a run weighted by (run_len - L + 1)
weights = np.array([max(0, len(r.group()) - L + 1) for r in runs], dtype=np.float64)
weights /= weights.sum()
pick_run = rng.choice(len(runs), size=N, p=weights)

seqs = []
for ri in pick_run:
    run = runs[ri].group()
    start = int(rng.integers(0, len(run) - L + 1))
    seqs.append(run[start:start + L])

with open(HERE / "sequences_0.txt", "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N} real chr22 fragments")
