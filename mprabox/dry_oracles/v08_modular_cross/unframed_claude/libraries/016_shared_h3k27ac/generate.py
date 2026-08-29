"""Shared H3K27ac peaks across K562 + HepG2 + SKNSH (broadly active enhancers).

Idea: rather than picking strong but cell-specific peaks, pick peaks active
in ALL THREE cell lines. These broadly active enhancers should activate
all three cell-line models simultaneously, lifting all three r columns
on eval_01.

Library:
- 25,000 shared-peak sequences (200bp centered on midpoint)
- 25,000 dinuc-shuffled null

Intersection method: bin midpoints into 500bp bins per chrom, take
intersection of (chrom, bin) sets across cells.
"""
from pathlib import Path
from pyfaidx import Fasta
import random

ROOT = Path(__file__).resolve().parents[2]
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

L = 200
BIN = 500


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


k562 = load_peaks(ROOT / "data" / "K562_H3K27ac.bed")
hepg2 = load_peaks(ROOT / "data" / "HepG2_H3K27ac.bed")
sknsh = load_peaks(ROOT / "data" / "SKNSH_H3K27ac.bed")
print(f"H3K27ac peaks: K562={len(k562):,}  HepG2={len(hepg2):,}  SKNSH={len(sknsh):,}")


def to_bins(peaks):
    """Map (chrom, bin) -> max signal in that bin."""
    bins = {}
    for chrom, mid, sig in peaks:
        b = mid // BIN
        key = (chrom, b)
        if key not in bins or bins[key][1] < sig:
            bins[key] = (mid, sig)
    return bins


k562_b = to_bins(k562)
hepg2_b = to_bins(hepg2)
sknsh_b = to_bins(sknsh)
shared_keys = set(k562_b) & set(hepg2_b) & set(sknsh_b)
print(f"Shared bins: {len(shared_keys):,}")

# Score each shared bin by min signal across cells (most consistently active)
shared = []
for k in shared_keys:
    mid_k, sig_k = k562_b[k]
    mid_h, sig_h = hepg2_b[k]
    mid_s, sig_s = sknsh_b[k]
    avg_mid = (mid_k + mid_h + mid_s) // 3
    min_sig = min(sig_k, sig_h, sig_s)
    shared.append((k[0], avg_mid, min_sig))

shared.sort(key=lambda x: -x[2])
print(f"Top shared min_signal: {shared[0][2]:.2f}")
print(f"Median shared min_signal: {shared[len(shared)//2][2]:.2f}")

fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
half = L // 2

# Only 5-6k unique shared peaks. Use jittered midpoints (±60bp) to get
# ~5 variants per peak, biologically equivalent (peak is broader than 200bp).
py_rng = random.Random(901)
JITTER = 60
N_PER_PEAK = 6
seen = set()
active = []
attempts_per_peak = N_PER_PEAK * 4
for chrom, mid, _ in shared:
    if len(active) >= 25_000:
        break
    chrom_len = len(fa[chrom])
    variants = 0
    for _ in range(attempts_per_peak):
        if variants >= N_PER_PEAK:
            break
        offset = py_rng.randint(-JITTER, JITTER)
        m = mid + offset
        s, e = m - half, m + half
        if s < 0 or e > chrom_len:
            continue
        key = (chrom, s)
        if key in seen:
            continue
        seq = fa[chrom][s:e]
        if len(seq) != L or "N" in seq:
            continue
        seen.add(key)
        active.append(seq)
        variants += 1
print(f"Extracted active: {len(active)}")

# If still short, take more from full shared list with jitter
while len(active) < 25_000:
    chrom, mid, _ = py_rng.choice(shared)
    chrom_len = len(fa[chrom])
    offset = py_rng.randint(-JITTER, JITTER)
    m = mid + offset
    s, e = m - half, m + half
    if s < 0 or e > chrom_len:
        continue
    key = (chrom, s)
    if key in seen:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    seen.add(key)
    active.append(seq)
active = active[:25_000]
print(f"Final active: {len(active)} (unique starts: {len(seen)})")


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


null = [dinuc_shuffle(s, py_rng) for s in active]
print(f"Null: {len(null)}")

combined = active + null
py_rng.shuffle(combined)
OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences (25k shared-H3K27ac + 25k dinuc-shuffled)")
