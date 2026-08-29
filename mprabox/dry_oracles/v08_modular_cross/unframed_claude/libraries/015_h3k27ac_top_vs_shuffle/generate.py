"""H3K27ac active enhancer peaks per cell line + dinucleotide-shuffled null.

H3K27ac marks ACTIVE enhancers specifically (vs DNase-accessible regions
which include poised). Should beat DHS-based selection (exp 010) because
the peaks are more specific to truly active regulatory elements.

Library composition:
- 8,333 K562 H3K27ac top peaks
- 8,333 HepG2 H3K27ac top peaks
- 8,333 SK-N-SH H3K27ac top peaks
- 25,000 dinucleotide-shuffled versions (mixed across the 3 cells)

200bp centered on each peak midpoint.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
import random

ROOT = Path(__file__).resolve().parents[2]
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N_PER_CELL_ACTIVE = 8333  # 8333*3 = 24999

def load_h3k27ac(path, signal_col=6):
    out = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if "_" in chrom or chrom in {"chrM", "chrEBV"}:
                continue
            start, end = int(parts[1]), int(parts[2])
            signal = float(parts[signal_col]) if len(parts) > signal_col else 0.0
            mid = (start + end) // 2
            out.append((chrom, mid, signal))
    return out

# Load peaks; format col 6 = signalValue (broadPeak)
k562 = load_h3k27ac(ROOT / "data" / "K562_H3K27ac.bed", signal_col=6)
hepg2 = load_h3k27ac(ROOT / "data" / "HepG2_H3K27ac.bed", signal_col=6)
sknsh = load_h3k27ac(ROOT / "data" / "SKNSH_H3K27ac.bed", signal_col=6)

print(f"H3K27ac peaks: K562={len(k562):,}  HepG2={len(hepg2):,}  SKNSH={len(sknsh):,}")

# Sort by signal descending
for lst in (k562, hepg2, sknsh):
    lst.sort(key=lambda x: -x[2])

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
half = L // 2

def extract(peaks, n_want):
    out = []
    for chrom, mid, _ in peaks:
        if len(out) >= n_want:
            break
        s, e = mid - half, mid + half
        chrom_len = len(fa[chrom])
        if s < 0 or e > chrom_len:
            continue
        seq = fa[chrom][s:e]
        if len(seq) != L or "N" in seq:
            continue
        out.append(seq)
    return out

# Take a random sample from the TOP 30k peaks per cell (not just absolute top,
# to avoid all being similar high-signal promoter-ish regions)
TOP_POOL = 40_000
py_rng = random.Random(801)
k562_pool = k562[:TOP_POOL]
hepg2_pool = hepg2[:TOP_POOL]
sknsh_pool = sknsh[:TOP_POOL]
py_rng.shuffle(k562_pool)
py_rng.shuffle(hepg2_pool)
py_rng.shuffle(sknsh_pool)

k562_seqs = extract(k562_pool, N_PER_CELL_ACTIVE)
hepg2_seqs = extract(hepg2_pool, N_PER_CELL_ACTIVE)
sknsh_seqs = extract(sknsh_pool, N_PER_CELL_ACTIVE)
print(f"Extracted: K562={len(k562_seqs)} HepG2={len(hepg2_seqs)} SKNSH={len(sknsh_seqs)}")

active = k562_seqs + hepg2_seqs + sknsh_seqs

# Dinucleotide-shuffle for null
def dinuc_shuffle(seq):
    n = len(seq)
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])
    for _ in range(50):
        e2 = {b: list(v) for b, v in edges.items()}
        for b in e2:
            py_rng.shuffle(e2[b])
        try:
            walk = [seq[0]]
            edge_iters = {b: iter(e2[b]) for b in "ACGT"}
            for _ in range(n - 1):
                cur = walk[-1]
                nxt = next(edge_iters[cur])
                walk.append(nxt)
            if len(walk) == n:
                return "".join(walk)
        except StopIteration:
            continue
    arr = list(seq); py_rng.shuffle(arr); return "".join(arr)

# top-up active to 25000
while len(active) < 25_000:
    pool = py_rng.choice([k562_pool, hepg2_pool, sknsh_pool])
    chrom, mid, _ = py_rng.choice(pool)
    s, e = mid - half, mid + half
    chrom_len = len(fa[chrom])
    if s < 0 or e > chrom_len:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    active.append(seq)
active = active[:25_000]

null = [dinuc_shuffle(s) for s in active]

combined = active + null
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences (25k H3K27ac top + 25k dinuc-shuffled)")
