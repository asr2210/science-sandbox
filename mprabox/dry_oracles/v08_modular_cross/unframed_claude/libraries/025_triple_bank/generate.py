"""Triple bank: K562 + HepG2 + SKNSH, each internally 50/50 active/null.

Per-cell maxima on eval_01 are mutually exclusive in homogeneous designs:
- K562 max: exp 012 (K562 sat GC=65/25) → +0.0089
- HepG2 max: exp 015 (real H3K27ac) → +0.0069
- SKNSH max: exp 024 (K562 motifs GC=60/40) → +0.0074

Split 50k into 3 banks, each engineered for its cell's best design.
Each bank internally is 50/50 active/null, so each cell's predictor sees
a clean signal within its bank, with other banks adding bounded noise.

- ~8333 K562 active + ~8333 K562 null (exp 012 design)
- ~8333 HepG2 H3K27ac active + ~8333 dinuc-shuffled
- ~8333 SKNSH-target active (K562 motifs GC=60) + ~8333 null GC=40
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

# For SKNSH bank, use exp 024's recipe (K562 motifs panel, GC=60/40)
SKNSH_TARGET_MOTIFS = K562_MOTIFS[:]

rng = np.random.default_rng(1801)
py_rng = random.Random(1801)
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


# K562 bank: exp 012 design
N_K = 8333
k562_active = bg(N_K, L, gc=0.65)
k562_active = insert(k562_active, K562_MOTIFS, n_per_seq=12)
k562_null = bg(N_K, L, gc=0.25)
k562_lines = ["".join(r) for r in k562_active] + ["".join(r) for r in k562_null]


# SKNSH bank: exp 024 design (K562 motifs GC=60 active + GC=40 null)
N_S = 8334
sknsh_active = bg(N_S, L, gc=0.60)
sknsh_active = insert(sknsh_active, SKNSH_TARGET_MOTIFS, n_per_seq=8)
sknsh_null = bg(N_S, L, gc=0.40)
sknsh_lines = ["".join(r) for r in sknsh_active] + ["".join(r) for r in sknsh_null]


# HepG2 bank: real H3K27ac peaks
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
hepg2_pool = hepg2_peaks[:30_000]
py_rng.shuffle(hepg2_pool)

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
N_H = 8333
hepg2_active_lines = []
for chrom, mid, _ in hepg2_pool:
    if len(hepg2_active_lines) >= N_H:
        break
    s, e = mid - half, mid + half
    chrom_len = len(fa[chrom])
    if s < 0 or e > chrom_len:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    hepg2_active_lines.append(seq)


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
hepg2_lines = hepg2_active_lines + hepg2_null_lines

combined = k562_lines + sknsh_lines + hepg2_lines
print(f"Bank sizes: K562={len(k562_lines)} SKNSH={len(sknsh_lines)} HepG2={len(hepg2_lines)} total={len(combined)}")
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences (triple bank: K562 syn + SKNSH-targeted + HepG2 real)")
