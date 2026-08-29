"""Experiment 006: DNase peaks + dinucleotide-preserving shuffles.

25,000 real DNase peaks (K562/HepG2/SK-N-SH mix) + 25,000 dinucleotide-
shuffled controls of those same peaks. Each real peak has a matching shuffle.

Rationale: prior experiments (001-005) showed model gets ~0 from real
sequences alone. A pos/neg contrast within the training set forces the
model to learn what distinguishes active from inactive sequence
*structure* at matched composition.

For generalization: the model that learns "motif grammar drives
activity, scrambled motifs don't" should transfer to OTHER cell types,
where the same motif vocabulary operates.
"""
import os
import gzip
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
N_REAL = 25_000  # 25k real peaks
N_SHUFFLE = 25_000  # 25k shuffled controls

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
PEAKS = {
    "K562":   os.path.join(ROOT, "data", "ENCFF821KDJ.bed.gz"),
    "HepG2":  os.path.join(ROOT, "data", "ENCFF341XEM.bed.gz"),
    "SK-N-SH":os.path.join(ROOT, "data", "ENCFF752OZB.bed.gz"),
}
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

def load_peaks(path):
    out = []
    with gzip.open(path, "rt") as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if "_" in chrom or chrom == "chrM":
                continue
            s, e = int(cols[1]), int(cols[2])
            out.append((chrom, s, e))
    return out

# Pool all peaks together
all_peaks = []
for cell, path in PEAKS.items():
    all_peaks.extend(load_peaks(path))
print(f"total peaks: {len(all_peaks)}")
rng.shuffle(all_peaks)

# Extract N_REAL sequences
real_seqs = []
for chrom, s, e in all_peaks:
    c = (s + e) // 2
    ss = c - L // 2
    ee = ss + L
    if ss < 0 or ee > len(fa[chrom]):
        continue
    seq = str(fa[chrom][ss:ee])
    if "N" in seq or len(seq) != L:
        continue
    real_seqs.append(seq)
    if len(real_seqs) == N_REAL:
        break

print(f"got {len(real_seqs)} real sequences")

# Dinucleotide shuffle (Markov-1 preserving)
def dinuc_shuffle(seq, rng):
    """Altschul-Erickson dinucleotide shuffle."""
    n = len(seq)
    # Build graph: from each nucleotide, list of next nucleotides
    edges = {}
    for i in range(n - 1):
        edges.setdefault(seq[i], []).append(seq[i + 1])
    # Eulerian walk
    # First shuffle the adjacency lists
    for k in edges:
        rng.shuffle(edges[k])
    # Pick first nucleotide
    out = [seq[0]]
    while len(out) < n:
        cur = out[-1]
        if cur in edges and edges[cur]:
            nxt = edges[cur].pop()
            out.append(nxt)
        else:
            # Stuck — fall back: pick from remaining
            remaining = [c for k, lst in edges.items() for c in lst]
            if not remaining:
                break
            out.append(remaining[int(rng.integers(0, len(remaining)))])
            # remove that one from edges
            for k, lst in edges.items():
                if lst and lst[0] == out[-1]:
                    lst.pop(0)
                    break
    if len(out) < n:
        out += list(seq[len(out):])
    return "".join(out)[:n]

shuffle_seqs = []
for s in real_seqs[:N_SHUFFLE]:
    shuffle_seqs.append(dinuc_shuffle(s, rng))

print(f"got {len(shuffle_seqs)} shuffles")

all_seqs = real_seqs + shuffle_seqs
assert len(all_seqs) == 50_000
rng.shuffle(all_seqs)

# Validate
for s in all_seqs:
    assert len(s) == L
    assert set(s) <= set("ACGT")

with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {len(all_seqs)} seqs to {OUT}")
