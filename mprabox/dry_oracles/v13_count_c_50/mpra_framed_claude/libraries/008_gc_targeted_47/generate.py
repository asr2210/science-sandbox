"""Experiment 008: GC-targeted natural genomic.

Sample 200bp windows uniformly across all 24 chromosomes (proportional to
length) but REJECT any window whose local GC content is outside [44%, 52%].

Tests theory v7: the eval_01 sweet spot is ~47% GC. A library whose
compositional distribution is tightly centered there, while remaining
natural (preserving motifs), should beat all-chrom (which has too much
low-GC) and multi-chrom-5 (which sampled chr19 heavily but had a wider GC).
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
GC_MIN = 0.44
GC_MAX = 0.52
DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
rng = np.random.default_rng(SEED)

fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
lengths = {c: len(fas[c][c]) for c in CHROMS}
total = sum(lengths.values())

# Proportional target
allocations = {}
remaining = N
for i, c in enumerate(CHROMS):
    if i == len(CHROMS) - 1:
        allocations[c] = remaining
    else:
        n_c = int(round(N * lengths[c] / total))
        allocations[c] = n_c
        remaining -= n_c

valid = set("ACGT")
all_seqs = []
total_attempts = 0
for c in CHROMS:
    target = allocations[c]
    chrom_len = lengths[c]
    collected = []
    while len(collected) < target:
        batch = rng.integers(0, chrom_len - L, size=max(20 * (target - len(collected)), 1000))
        for start in batch:
            if len(collected) >= target:
                break
            total_attempts += 1
            s = fas[c][c][int(start):int(start) + L]
            if len(s) != L or not set(s).issubset(valid):
                continue
            gc = (s.count("G") + s.count("C")) / L
            if GC_MIN <= gc <= GC_MAX:
                collected.append(s)
    all_seqs.extend(collected)
    print(f"{c}: {target} kept (running attempts ~{total_attempts/1e6:.1f}M)")

assert len(all_seqs) == N
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")

# Sanity check: GC distribution
import numpy as _np
gcs = _np.array([(s.count("G") + s.count("C")) / L for s in all_seqs])
print(f"GC stats: mean={gcs.mean():.3f}, std={gcs.std():.3f}, "
      f"range=[{gcs.min():.3f}, {gcs.max():.3f}]")
print(f"Wrote {N} sequences (GC-targeted [{GC_MIN}, {GC_MAX}]).")
