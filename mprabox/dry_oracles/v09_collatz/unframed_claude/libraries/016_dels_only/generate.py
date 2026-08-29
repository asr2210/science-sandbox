"""Experiment 016 — cCRE dELS (distal enhancer-like) only.

50k 200bp windows centered on ENCODE cCRE V4 dELS elements from
chr1/18/19/22. dELS are distal enhancer-like — should be naturalistic
(unlike promoter PLS) and enriched for active enhancer features.

Compare vs exp 010 (mixed cCRE classes: 0.3077) and exp 009 (chr22
random: 0.3202).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(16)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
chroms = ("chr1", "chr18", "chr19", "chr22")
chrom_seq = {}
for name in chroms:
    parts = []
    with (ROOT / "data" / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"): continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)
    print(f"{name}: {len(chrom_seq[name]):,}")

# Load dELS regions
dels = []
with (ROOT / "data" / "GRCh38-cCREs.bed").open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6: continue
        if parts[5] != "dELS": continue
        if parts[0] not in chrom_seq: continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        dels.append((parts[0], s, e))
print(f"dELS on our chroms: {len(dels):,}")

out = Path(__file__).parent / "sequences_0.txt"
seqs = []
while len(seqs) < N:
    idx = int(rng.integers(0, len(dels)))
    ch, s, e = dels[idx]
    mid = (s + e) // 2
    # small random jitter ±50bp to avoid being centered exactly
    jitter = int(rng.integers(-50, 51))
    ps = mid + jitter - L // 2
    pe = ps + L
    if ps < 0 or pe > len(chrom_seq[ch]): continue
    s2 = chrom_seq[ch][ps:pe]
    if "N" in s2: continue
    if any(s2.count(c * 20) > 0 for c in "ACGT"): continue
    seqs.append(s2)

rng.shuffle(seqs)
seqs = seqs[:N]

with out.open("w") as f:
    for s in seqs:
        f.write(s); f.write("\n")
print(f"Wrote {len(seqs)} to {out}")

# Diagnostics
gcs = [(seq.count("G") + seq.count("C")) / L for seq in seqs[:5000]]
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f} min={min(gcs):.2f} max={max(gcs):.2f}")
