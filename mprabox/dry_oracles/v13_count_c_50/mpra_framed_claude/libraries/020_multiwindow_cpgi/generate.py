"""
Experiment 020: Multi-window CpGi too (extending exp 019's technique).

Exp 019 applied 5-window augmentation to cCRE → +0.0003 mean.
Test if same technique applied to CpGi (1k unique × 5 windows = 5k)
gives further lift. If multi-windowing generalizes, both sources
benefit.

Composition:
- 22,500 random genomic (45%)
- 20,000 cCRE windows (4k unique × 5 offsets) (40%)
- 5,000 CpGi windows (1k unique × 5 offsets) (10%)
- 1,250 uniform random (2.5%)
- 1,250 mono-shuffled cCRE (2.5%)
"""
import os
from collections import defaultdict
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 0
OFFSETS = [-200, -100, 0, 100, 200]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FA_PATH = os.path.join(ROOT, "data", "hg38.fa")
BED_PATH = os.path.join(ROOT, "data", "cCRE_v3_primary.bed")
CPG_PATH = os.path.join(ROOT, "data", "cpg_islands.bed")
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
PRIM = set(CHROMS)

CLASS_FROM_LABEL = lambda label: label.split(",", 1)[0]
COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
def revcomp(s):
    return "".join(COMP[b] for b in reversed(s))

def sample_random_genomic(rng, fa, n):
    lengths = {c: len(fa[c]) for c in CHROMS}
    weights = np.array([lengths[c] for c in CHROMS], dtype=float)
    weights /= weights.sum()
    seqs = []
    while len(seqs) < n:
        chrom = CHROMS[rng.choice(len(CHROMS), p=weights)]
        start = rng.integers(0, lengths[chrom] - L)
        s = str(fa[chrom][start:start + L]).upper()
        if "N" in s:
            continue
        if rng.random() < 0.5:
            s = revcomp(s)
        seqs.append(s)
    return seqs

def sample_ccre_multiwindow(rng, fa, n_unique):
    """Sample n_unique cCREs (class-balanced), take len(OFFSETS) windows
    each at each offset from center."""
    buckets = defaultdict(list)
    with open(BED_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            buckets[CLASS_FROM_LABEL(parts[4])].append((parts[0], int(parts[1]), int(parts[2])))
    classes = sorted(buckets.keys())
    n_each = n_unique // len(classes)
    remainder = n_unique - n_each * len(classes)
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    seqs = []
    for ci, cls in enumerate(classes):
        n_target = n_each + (1 if ci < remainder else 0)
        idx_perm = rng.permutation(len(buckets[cls]))
        taken = 0
        for i in idx_perm:
            chrom, s, e = buckets[cls][int(i)]
            mid = (s + e) // 2
            # Check that all windows fit
            windows = []
            ok = True
            for off in OFFSETS:
                ws = mid - L // 2 + off
                we = ws + L
                if ws < 0 or we > chrom_len[chrom]:
                    ok = False
                    break
                seq = str(fa[chrom][ws:we]).upper()
                if "N" in seq:
                    ok = False
                    break
                if rng.random() < 0.5:
                    seq = revcomp(seq)
                windows.append(seq)
            if not ok:
                continue
            seqs.extend(windows)
            taken += 1
            if taken == n_target:
                break
    return seqs

def sample_cpgi_multiwindow(rng, fa, n_unique):
    """Sample n_unique CpGi anchors, take len(OFFSETS) windows each."""
    elems = []
    with open(CPG_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in PRIM:
                continue
            elems.append((chrom, int(parts[1]), int(parts[2])))
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    idx_perm = rng.permutation(len(elems))
    seqs = []
    taken = 0
    for i in idx_perm:
        chrom, s, e = elems[int(i)]
        mid = (s + e) // 2
        windows = []
        ok = True
        for off in OFFSETS:
            ws = mid - L // 2 + off
            we = ws + L
            if ws < 0 or we > chrom_len[chrom]:
                ok = False
                break
            seq = str(fa[chrom][ws:we]).upper()
            if "N" in seq:
                ok = False
                break
            if rng.random() < 0.5:
                seq = revcomp(seq)
            windows.append(seq)
        if not ok:
            continue
        seqs.extend(windows)
        taken += 1
        if taken == n_unique:
            break
    return seqs

def sample_uniform_random(rng, n):
    bases = np.array(list("ACGT"))
    arr = rng.integers(0, 4, size=(n, L))
    return ["".join(bases[row]) for row in arr]

def sample_mono_shuffled_ccre(rng, fa, n_total):
    all_ccre = []
    with open(BED_PATH) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            all_ccre.append((parts[0], int(parts[1]), int(parts[2])))
    chrom_len = {c: len(fa[c]) for c in CHROMS}
    idx_perm = rng.permutation(len(all_ccre))
    seqs = []
    for i in idx_perm:
        chrom, s, e = all_ccre[int(i)]
        mid = (s + e) // 2
        ws, we = mid - L // 2, mid - L // 2 + L
        if ws < 0 or we > chrom_len[chrom]:
            continue
        seq = str(fa[chrom][ws:we]).upper()
        if "N" in seq:
            continue
        bases = list(seq)
        rng.shuffle(bases)
        seqs.append("".join(bases))
        if len(seqs) == n_total:
            break
    return seqs

def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(FA_PATH)
    a = sample_random_genomic(rng, fa, 22500); print(f"genomic: {len(a)}")
    b = sample_ccre_multiwindow(rng, fa, 4000); print(f"cCRE 5x-windowed: {len(b)} (from 4k unique)")
    c = sample_cpgi_multiwindow(rng, fa, 1000); print(f"CpGi 5x-windowed: {len(c)} (from 1k unique)")
    d = sample_uniform_random(rng, 1250); print(f"uniform: {len(d)}")
    e = sample_mono_shuffled_ccre(rng, fa, 1250); print(f"mono-shuf: {len(e)}")
    combined = a + b + c + d + e
    rng.shuffle(combined)
    with open(OUT, "w") as fout:
        fout.write("\n".join(combined) + "\n")
    with open(OUT) as fin:
        lines = fin.read().splitlines()
    assert len(lines) == N
    for l in lines[:5]:
        assert len(l) == L and set(l) <= set("ACGT")
    print(f"wrote {len(lines)} sequences")

if __name__ == "__main__":
    main()
