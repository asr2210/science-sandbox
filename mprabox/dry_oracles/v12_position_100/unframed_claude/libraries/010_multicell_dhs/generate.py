"""Exp 010: aggressive multi-cell DHS library.

Pool all DNase peaks from K562 + HepG2 + SK-N-SH (15 files total),
dedupe (chrom, summit), keep top 50k by max smoothed_peak_height.
Tests whether broad cell-type DHS coverage breaks 0.08.
"""
import os
import gzip
import glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded", len(CHRS), "chromosomes")

best = {}  # (chr, summit) -> height
narrowPeak_pattern = ("sknsh_",)
for path in sorted(glob.glob(os.path.join(DATA, "k562_*.bed.gz")) +
                   glob.glob(os.path.join(DATA, "hepg2_*.bed.gz")) +
                   glob.glob(os.path.join(DATA, "sknsh_*.bed.gz"))):
    is_narrowpeak = os.path.basename(path).startswith(narrowPeak_pattern)
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if is_narrowpeak:
                # narrowPeak: chrom start end name score strand signalValue pValue qValue peak(offset)
                if len(parts) < 10:
                    continue
                try:
                    chrom = parts[0]
                    s, e = int(parts[1]), int(parts[2])
                    offset = int(parts[9])
                    if offset < 0:
                        summit = (s + e) // 2
                    else:
                        summit = s + offset
                    height = float(parts[6])  # signalValue
                except ValueError:
                    continue
            else:
                # ENCODE custom: chrom start end id max_density summit_density summit smoothed_peak_height
                if len(parts) < 8:
                    continue
                try:
                    chrom = parts[0]
                    summit = int(parts[6])
                    height = float(parts[7])
                except ValueError:
                    continue
            if chrom not in CHRS:
                continue
            k = (chrom, summit)
            if height > best.get(k, -1):
                best[k] = height
print("unique summits across 3 cells:", len(best))

# Sort by height desc.
items = sorted(best.items(), key=lambda kv: -kv[1])

acgt = set("ACGT")
seqs = []
seen_positions = set()  # dedupe near-duplicates: round summit to nearest 50bp
for (chrom, summit), _ in items:
    bucket = (chrom, summit // 50)
    if bucket in seen_positions:
        continue
    seen_positions.add(bucket)
    seq = CHRS[chrom]
    s = summit - HALF
    if s < 0 or s + L > len(seq):
        continue
    w = seq[s:s + L]
    if set(w) <= acgt:
        seqs.append(w)
    if len(seqs) >= N:
        break
print(f"got {len(seqs)} DHS sequences (after 50bp dedupe)")

# Pad if necessary.
rng = np.random.default_rng(37)
chr_keys = list(CHRS.keys())
weights = np.array([len(CHRS[k]) for k in chr_keys], dtype=np.float64)
weights /= weights.sum()
while len(seqs) < N:
    ck = chr_keys[rng.choice(len(chr_keys), p=weights)]
    c = CHRS[ck]
    s = rng.integers(0, len(c) - L + 1)
    w = c[s:s + L]
    if set(w) <= acgt:
        seqs.append(w)

with open(OUT, "w") as f:
    f.write("\n".join(seqs[:N]) + "\n")
print(f"wrote {OUT}: {N} x {L}")
