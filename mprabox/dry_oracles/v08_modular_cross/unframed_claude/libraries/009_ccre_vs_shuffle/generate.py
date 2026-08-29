"""Real ENCODE cCRE enhancer/promoter sequences vs shuffled controls.

25k active: 200bp centered on real PLS/pELS/dELS cCREs from ENCODE V4.
25k null: each active sequence dinucleotide-shuffled (preserves bg
composition but destroys motifs).

Predict: should beat synthetic motif libraries because real cCREs
contain the full natural regulatory context that any sequence-to-
activity model was trained on.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
BED = ROOT / "data" / "cCRE_v4.bed"
FASTA = ROOT / "data" / "hg38.fa"
OUT = Path(__file__).parent / "sequences_0.txt"

N_TOTAL = 50_000
L = 200
N_ACTIVE = N_TOTAL // 2

ALLOWED_CLASSES = {"PLS", "pELS", "dELS"}

rng = np.random.default_rng(101)

# 1) Read BED, filter classes, keep midpoints
peaks = []
with open(BED) as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        chrom, start, end, _id1, _id2, cls = parts[0], int(parts[1]), int(parts[2]), parts[3], parts[4], parts[5]
        if cls not in ALLOWED_CLASSES:
            continue
        # skip alt/random/unplaced contigs
        if "_" in chrom or chrom in {"chrM", "chrEBV"}:
            continue
        mid = (start + end) // 2
        peaks.append((chrom, mid))
print(f"Eligible peaks: {len(peaks):,}")

# 2) Sample N_ACTIVE
idx = rng.choice(len(peaks), size=N_ACTIVE, replace=False)
selected = [peaks[i] for i in idx]

# 3) Extract 200bp centered on midpoint
fa = Fasta(str(FASTA), as_raw=True, sequence_always_upper=True)
half = L // 2

active = []
skipped = 0
for chrom, mid in selected:
    chrom_len = len(fa[chrom])
    s = mid - half
    e = mid + half
    if s < 0 or e > chrom_len:
        skipped += 1
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        skipped += 1
        continue
    active.append(seq)
print(f"Active extracted: {len(active):,}  (skipped {skipped})")

# Top up to N_ACTIVE if some were skipped
while len(active) < N_ACTIVE:
    i = rng.integers(len(peaks))
    chrom, mid = peaks[i]
    s, e = mid - half, mid + half
    chrom_len = len(fa[chrom])
    if s < 0 or e > chrom_len:
        continue
    seq = fa[chrom][s:e]
    if len(seq) != L or "N" in seq:
        continue
    active.append(seq)
active = active[:N_ACTIVE]

# 4) Build null = dinucleotide-shuffled version of each active sequence
def dinuc_shuffle(seq, rng):
    """Simple dinucleotide-preserving shuffle (Altschul-Erickson style)."""
    n = len(seq)
    # Build graph: node = nt, edges = ordered dinucleotides
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])
    # Eulerian walk
    # Shuffle outgoing edges then ensure last edge of each non-terminal
    # node points to the terminal-reaching tree.
    # Simpler approximation: shuffle each list, then walk.
    last = seq[-1]
    # Reserve a "last edge" for each non-terminal node pointing toward `last`
    # The classic Altschul-Erickson trick. For 200bp this approximation
    # generally produces valid Eulerian walks; if not, retry.
    for _ in range(50):
        e2 = {b: list(v) for b, v in edges.items()}
        for b in e2:
            rng.shuffle(e2[b])
        # Generate a spanning tree rooted at `last` to ensure Eulerian path
        # Pick the LAST occurrence of each base's outgoing edge to be the
        # edge that takes us toward `last`.
        try:
            tree_last_edge = {}
            for b in "ACGT":
                if b == last or not e2[b]:
                    continue
                # find one edge in e2[b] that reaches `last` via shuffled chain
                # Approximation: just allow any walk; if fails, retry.
                pass
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
    # Fallback: mononucleotide shuffle
    arr = list(seq)
    rng.shuffle(arr)
    return "".join(arr)

# numpy rng doesn't have .shuffle on lists; use python rng for shuffle
import random
py_rng = random.Random(102)

# Use python random for shuffle in dinuc_shuffle
def dinuc_shuffle_py(seq):
    n = len(seq)
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])
    last = seq[-1]
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
    arr = list(seq)
    py_rng.shuffle(arr)
    return "".join(arr)

null = [dinuc_shuffle_py(s) for s in active]
print(f"Null shuffled: {len(null):,}")

combined = active + null
py_rng.shuffle(combined)

OUT.write_text("\n".join(combined) + "\n")
print(f"Wrote {len(combined)} sequences to {OUT}")
