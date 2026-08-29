"""Experiment 9: Natural hg38 sequences stratified by GC content.

Sample random 200bp windows from hg38 chr1 + chr22, but stratify them so the
realized GC distribution is approximately uniform on [0.20, 0.80] (vs the
natural ~0.43 mean / 0.099 std). Tests whether combining naturalness with
forced compositional spread beats either alone.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=9)
N, L = 50000, 200
N_BINS = 30  # GC bins
GC_LO, GC_HI = 0.20, 0.80
per_bin = N // N_BINS  # roughly 1666 per bin

DATA = Path(__file__).resolve().parents[2] / "data"

def load_fa(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return "".join(line for line in lines if not line.startswith(">")).upper()

chrom_seq = {"chr1": load_fa(DATA / "chr1.fa"),
             "chr22": load_fa(DATA / "chr22.fa")}
print(f"chr1: {len(chrom_seq['chr1']):,}; chr22: {len(chrom_seq['chr22']):,}")

valid = re.compile(r"^[ACGT]+$")
bin_buckets = {i: [] for i in range(N_BINS)}
bin_width = (GC_HI - GC_LO) / N_BINS

def gc_bin(window):
    gc = (window.count("G") + window.count("C")) / L
    if gc < GC_LO or gc >= GC_HI:
        return None
    return min(int((gc - GC_LO) / bin_width), N_BINS - 1)

chroms = list(chrom_seq.keys())
chrom_lens = np.array([len(chrom_seq[c]) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

attempts = 0
filled = 0
target_per_bin = per_bin
while filled < N_BINS or any(len(b) < target_per_bin for b in bin_buckets.values()):
    ci = int(rng.choice(len(chroms), p=weights))
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    win = chrom_seq[chroms[ci]][pos:pos + L]
    attempts += 1
    if not valid.match(win):
        continue
    b = gc_bin(win)
    if b is None:
        continue
    if len(bin_buckets[b]) < target_per_bin:
        bin_buckets[b].append(win)
        if len(bin_buckets[b]) == target_per_bin:
            filled += 1
            print(f"  bin {b} filled ({filled}/{N_BINS}) at attempt {attempts}")
    if attempts > 50_000_000:
        print(f"  attempt cap reached")
        break

out = []
for b in range(N_BINS):
    out.extend(bin_buckets[b])
# Pad with extras if any bin underfilled
remaining = N - len(out)
if remaining > 0:
    print(f"  padding {remaining} from random unbinned")
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
print(f"Wrote {len(out)} natural-stratified sequences (attempts={attempts:,})")

arr = np.array([[ord(b) for b in s] for s in out[:10000]], dtype=np.int8)
C, G = ord('C'), ord('G')
gc = ((arr == C) | (arr == G)).mean(axis=1)
print(f"GC% (sample of 10k): mean={gc.mean():.3f}, std={gc.std():.3f}, "
      f"min={gc.min():.3f}, max={gc.max():.3f}")
