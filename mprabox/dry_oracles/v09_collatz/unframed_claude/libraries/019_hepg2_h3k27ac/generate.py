"""Experiment 019 — HepG2 H3K27ac peaks (active enhancers).

H3K27ac marks ACTIVE enhancers (stronger signal than DHS-only).
Use HepG2 H3K27ac peaks (ENCFF580KMC, 41544 peaks). Center 200bp
windows on peak summits when available, else peak midpoint.

Goal: if HepG2 model rewards "active" sequences, this might push
HepG2 past its 0.20 ceiling.
"""
import gzip
import numpy as np
from pathlib import Path

rng = np.random.default_rng(19)
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

peaks = []
with gzip.open(ROOT / "data" / "hepg2_h3k27ac.bed.gz", "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3 or parts[0].startswith(("#", "chrom", "track")):
            continue
        ch = parts[0]
        if ch not in chrom_seq:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        # narrowPeak summit (col 10, 0-based offset) — if present
        summit = None
        if len(parts) >= 10:
            try:
                offset = int(parts[9])
                summit = s + offset
            except ValueError:
                pass
        if summit is None:
            summit = (s + e) // 2
        peaks.append((ch, summit))
print(f"peaks on our chroms: {len(peaks)}")

out = Path(__file__).parent / "sequences_0.txt"
seqs = []
while len(seqs) < N:
    idx = int(rng.integers(0, len(peaks)))
    ch, summit = peaks[idx]
    jitter = int(rng.integers(-100, 101))
    ps = summit + jitter - L // 2
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

gcs = [(s.count("G") + s.count("C")) / L for s in seqs[:5000]]
print(f"Wrote {len(seqs)}; GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
