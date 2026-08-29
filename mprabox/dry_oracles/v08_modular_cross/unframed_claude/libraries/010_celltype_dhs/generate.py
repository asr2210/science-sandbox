"""Cell-type-specific DHS peaks from ENCODE for K562/HepG2/SK-N-SH.

Use top-signal DNase narrowPeaks from each cell line; extract 200bp
centered on each peak's summit (or midpoint).

Library composition:
- 16,667 K562 top-signal peaks
- 16,667 HepG2 top-signal peaks
- 16,666 SK-N-SH top-signal peaks

No explicit null — the cross-cell-line variation creates the variance
each cell-line model will see (K562 model: K562 peaks high, others lower).

Predict: each cell line's r should jump because the library cleanly
spans high/low activity per cell line.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
N_PER_CELL = [16667, 16667, 16666]

def load_narrowpeak(path, signal_col=6, summit_col=None):
    """Returns list of (chrom, mid, signal)."""
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
            if summit_col is not None and len(parts) > summit_col:
                try:
                    mid = int(parts[summit_col])
                except ValueError:
                    mid = (start + end) // 2
            else:
                mid = (start + end) // 2
            out.append((chrom, mid, signal))
    return out

# Load
k562 = load_narrowpeak(ROOT / "data" / "K562_dnase.bed", signal_col=6)
sknsh = load_narrowpeak(ROOT / "data" / "SKNSH_dnase.bed", signal_col=6)
# HepG2 has different format: chr start end id max_density summit_density summit smoothed_peak_height
hepg2 = load_narrowpeak(ROOT / "data" / "HepG2_dnase.bed", signal_col=4, summit_col=6)

print(f"Peaks loaded: K562={len(k562):,}  HepG2={len(hepg2):,}  SKNSH={len(sknsh):,}")

# Sort by signal descending and take top N
k562.sort(key=lambda x: -x[2])
hepg2.sort(key=lambda x: -x[2])
sknsh.sort(key=lambda x: -x[2])

print(f"K562  signal range: {k562[0][2]:.2f} → {k562[-1][2]:.2f}")
print(f"HepG2 signal range: {hepg2[0][2]:.2f} → {hepg2[-1][2]:.2f}")
print(f"SKNSH signal range: {sknsh[0][2]:.2f} → {sknsh[-1][2]:.2f}")

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
half = L // 2

def extract(peaks, n_want):
    out = []
    for chrom, mid, _ in peaks:
        if len(out) >= n_want:
            break
        chrom_len = len(fa[chrom])
        s, e = mid - half, mid + half
        if s < 0 or e > chrom_len:
            continue
        seq = fa[chrom][s:e]
        if len(seq) != L or "N" in seq:
            continue
        out.append(seq)
    return out

k562_seqs = extract(k562, N_PER_CELL[0])
hepg2_seqs = extract(hepg2, N_PER_CELL[1])
sknsh_seqs = extract(sknsh, N_PER_CELL[2])
print(f"Extracted: K562={len(k562_seqs)}  HepG2={len(hepg2_seqs)}  SKNSH={len(sknsh_seqs)}")

import random
py_rng = random.Random(303)
combined = k562_seqs + hepg2_seqs + sknsh_seqs
assert len(combined) == 50_000, len(combined)
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences to {OUT}")
