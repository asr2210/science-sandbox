"""Real K562 H3K27ac peaks + inserted K562 motifs to augment.

Real DHS/H3K27ac peaks alone gave NEGATIVE K562 on eval_01 (exp 010, 015).
But synthetic K562 motifs at GC=65 gave +0.0089 (exp 012).

Hypothesis: real peaks have natural enhancer context but the models'
training maybe expects more motifs than naturally occur. Augment real
K562 peaks with extra K562 motifs to combine "natural" + "saturated".

Composition:
- 25k real K562 H3K27ac peaks with 6 extra inserted K562 motifs
- 25k dinuc-shuffled (natural composition null)
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta
import random

ROOT = Path(__file__).resolve().parents[2]
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
half = L // 2

K562_MOTIFS = [
    "AGATAA", "TGATAA", "AGATAG", "TGATAG",
    "CACCC", "GGGGTG", "GGGTGGGG",
    "TGCTGAGTCAGCA",
    "CAGCTG", "CATCTG", "CACCTG",
    "TGAGTCA", "TGACTCA",
    "GGGCGG", "GGGCGGGG",
    "GGAAGT", "CGGAAG",
    "CCAAT",
    "TGACGTCA",
    "CACGTG",
]

py_rng = random.Random(1901)
rng = np.random.default_rng(1901)
COMP = str.maketrans("ACGT", "TGCA")


def load_peaks(path, signal_col=6):
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


k562_peaks = load_peaks(ROOT / "data" / "K562_H3K27ac.bed")
k562_peaks.sort(key=lambda x: -x[2])
print(f"K562 H3K27ac: {len(k562_peaks):,}")

TOP_POOL = 40_000
k562_pool = k562_peaks[:TOP_POOL]
py_rng.shuffle(k562_pool)

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)

active_lines = []
for chrom, mid, _ in k562_pool:
    if len(active_lines) >= 25_000:
        break
    s, e = mid - half, mid + half
    chrom_len = len(fa[chrom])
    if s < 0 or e > chrom_len:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    active_lines.append(seq)
print(f"Real K562 active: {len(active_lines)}")


def insert_motifs(seq, motifs, n):
    arr = list(seq)
    for _ in range(n):
        m = motifs[rng.integers(len(motifs))]
        if rng.random() < 0.5:
            m = m.translate(COMP)[::-1]
        ml = len(m)
        if ml >= len(arr):
            continue
        pos = rng.integers(0, len(arr) - ml + 1)
        arr[pos:pos + ml] = list(m)
    return "".join(arr)


augmented = [insert_motifs(s, K562_MOTIFS, n=6) for s in active_lines]
print(f"Augmented sample: {augmented[0]}")


def dinuc_shuffle(seq, rng):
    n = len(seq)
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        if seq[i] in edges:
            edges[seq[i]].append(seq[i + 1])
    for _ in range(50):
        e2 = {b: list(v) for b, v in edges.items()}
        for b in e2:
            rng.shuffle(e2[b])
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
    arr = list(seq); rng.shuffle(arr); return "".join(arr)


# Null = dinuc-shuffled augmented (preserves dinuc composition INCLUDING
# motif contributions; tests if motif IDENTITY vs composition matters)
null = [dinuc_shuffle(s, py_rng) for s in augmented]

combined = augmented + null
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} (25k real-K562-H3K27ac+6motifs + 25k dinuc-shuf)")
