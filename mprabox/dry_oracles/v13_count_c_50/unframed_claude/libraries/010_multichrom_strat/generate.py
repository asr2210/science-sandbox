"""Experiment 10: Multi-chromosome natural sequences, GC-stratified.

Sample 200bp windows from hg38 chr1, chr7, chr18, chr19, chr22 (mix of
chromosome compositions: chr19 is the most GC-rich autosome, chr18 is GC-poor,
chr7 is large/typical, chr1 large, chr22 small).

Stratify by GC into 40 bins from [0.18, 0.78] for stronger forced spread than
exp 9 (30 bins, [0.20, 0.80]).
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=10)
N, L = 50000, 200
N_BINS = 40
GC_LO, GC_HI = 0.18, 0.78
per_bin = N // N_BINS

DATA = Path(__file__).resolve().parents[2] / "data"

def load_fa(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return "".join(line for line in lines if not line.startswith(">")).upper()

print("Loading chromosomes...")
chrom_seq = {c: load_fa(DATA / f"{c}.fa") for c in ["chr1", "chr7", "chr18", "chr19", "chr22"]}
for c, s in chrom_seq.items():
    gc = (s.count("G") + s.count("C")) / max(1, s.count("G") + s.count("C") + s.count("A") + s.count("T"))
    print(f"  {c}: {len(s):,} bp, GC={gc:.3f}")

valid = re.compile(r"^[ACGT]+$")
bin_buckets = {i: [] for i in range(N_BINS)}
bin_width = (GC_HI - GC_LO) / N_BINS

chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

def gc_bin(window):
    gc = (window.count("G") + window.count("C")) / L
    if gc < GC_LO or gc >= GC_HI:
        return None
    return min(int((gc - GC_LO) / bin_width), N_BINS - 1)

attempts = 0
filled = 0
while filled < N_BINS:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if not valid.match(win):
        continue
    b = gc_bin(win)
    if b is None:
        continue
    if len(bin_buckets[b]) < per_bin:
        bin_buckets[b].append(win)
        if len(bin_buckets[b]) == per_bin:
            filled += 1
            if filled % 5 == 0:
                print(f"  {filled}/{N_BINS} bins filled at attempt {attempts:,}")
    if attempts > 50_000_000:
        print("attempt cap")
        break

out = []
for b in range(N_BINS):
    out.extend(bin_buckets[b])
# Pad if needed
remaining = N - len(out)
while remaining > 0:
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    if valid.match(win):
        out.append(win)
        remaining -= 1
out = out[:N]
rng.shuffle(out)
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out) + "\n")
print(f"Wrote {len(out)}, attempts={attempts:,}")

arr = np.array([[ord(b) for b in s] for s in out[:10000]], dtype=np.int8)
gc = ((arr == ord('C')) | (arr == ord('G'))).mean(axis=1)
print(f"GC% (10k sample): mean={gc.mean():.3f}, std={gc.std():.3f}, "
      f"range=[{gc.min():.3f}, {gc.max():.3f}]")
