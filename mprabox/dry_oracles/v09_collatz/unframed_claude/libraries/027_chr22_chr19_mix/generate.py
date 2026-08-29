"""Experiment 027 — chr22 + chr19 50/50 mix.

Both chr22 and chr19 are top scorers (0.3202 and 0.3198). Both near
47-48% GC. Mixing them maintains the natural composition with broader
sampling. Test if cross-chromosomal diversity adds anything.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(27)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
chrom_seq = {}
for name in ("chr22", "chr19"):
    parts = []
    with (ROOT / "data" / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"): continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)

def sample(name, k):
    seq = chrom_seq[name]
    out = []
    while len(out) < k:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        out.append(s)
    return out

per = N // 2
all_seqs = sample("chr22", per) + sample("chr19", N - per)
rng.shuffle(all_seqs)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for s in all_seqs:
        f.write(s); f.write("\n")
print(f"Wrote {len(all_seqs)}")
