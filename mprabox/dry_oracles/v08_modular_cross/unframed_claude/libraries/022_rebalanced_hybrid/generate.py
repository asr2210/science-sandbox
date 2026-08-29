"""Rebalanced hybrid: more K562 weight (16.5k each) + smaller HepG2 (8.5k each).

K562 contributes most variance per unit bank size. Lifting K562 weight
from 12.5k → 16.5k should push K562 r toward +0.0060+. HepG2 drops to
8.5k → r ≈ +0.0025. Target mean +0.0050.

Composition:
- 16,500 K562 syn active (GC=65, 12 K562 motifs)
- 16,500 K562 null (GC=25)
- 8,500 HepG2 H3K27ac real peaks
- 8,500 dinuc-shuffled HepG2 peaks
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

rng = np.random.default_rng(1501)
py_rng = random.Random(1501)
bases = np.array(list("ACGT"))
COMP = str.maketrans("ACGT", "TGCA")


def bg(n, length, gc):
    probs = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    return rng.choice(bases, size=(n, length), p=probs)


def insert(seqs, motifs, n_per_seq):
    for i in range(seqs.shape[0]):
        for _ in range(n_per_seq):
            m = motifs[rng.integers(len(motifs))]
            if rng.random() < 0.5:
                m = m.translate(COMP)[::-1]
            ml = len(m)
            pos = rng.integers(0, seqs.shape[1] - ml + 1)
            seqs[i, pos:pos + ml] = list(m)
    return seqs


N_K562 = 16_500
N_HEPG2 = 8_500

k562_active = bg(N_K562, L, gc=0.65)
k562_active = insert(k562_active, K562_MOTIFS, n_per_seq=12)
k562_null = bg(N_K562, L, gc=0.25)
k562_active_lines = ["".join(r) for r in k562_active]
k562_null_lines = ["".join(r) for r in k562_null]


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


hepg2_peaks = load_peaks(ROOT / "data" / "HepG2_H3K27ac.bed")
hepg2_peaks.sort(key=lambda x: -x[2])
TOP_POOL = 30_000
hepg2_pool = hepg2_peaks[:TOP_POOL]
py_rng.shuffle(hepg2_pool)

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
hepg2_active_lines = []
for chrom, mid, _ in hepg2_pool:
    if len(hepg2_active_lines) >= N_HEPG2:
        break
    s, e = mid - half, mid + half
    chrom_len = len(fa[chrom])
    if s < 0 or e > chrom_len:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    hepg2_active_lines.append(seq)
print(f"HepG2 active: {len(hepg2_active_lines)}")


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


hepg2_null_lines = [dinuc_shuffle(s, py_rng) for s in hepg2_active_lines]

combined = k562_active_lines + k562_null_lines + hepg2_active_lines + hepg2_null_lines
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} (16.5k K562 sat + 16.5k null + 8.5k HepG2 real + 8.5k shuffled)")
