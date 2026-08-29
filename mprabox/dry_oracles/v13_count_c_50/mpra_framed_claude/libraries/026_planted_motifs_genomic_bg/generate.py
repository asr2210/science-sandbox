"""
Experiment 026: Planted TF motifs in GENOMIC backgrounds, 2.5% dose.

Test theory v7.0: planted motifs failed in exp 025 because random
background broke motif transfer. Try the same motif palette but
plant into real genomic 200bp windows, at a smaller dose (2.5%).

Composition:
- 18,750 random genomic (37.5%)
- 20,000 cCRE (4k × 5-window) (40%)
- 5,000 CpGi (1k × 5-window) (10%)
- 1,250 planted-motif synthetic (genomic bg) (2.5%)
- 2,500 random genomic to back-fill (added to a)
- 1,250 uniform random (2.5%)
- 1,250 mono-shuffled cCRE (2.5%)

Net: 18.75k+20k+5k+1.25k+1.25k+1.25k+2.5k=... actually let me recompute:
   genomic=18,750 cCRE=20,000 CpGi=5,000 planted=1,250 uniform=1,250 shuf=1,250
   wait that's 47.5k, need 50k. Use genomic=21,250.

Final composition:
- 21,250 random genomic (42.5%)
- 20,000 cCRE (4k × 5-window) (40%)
- 5,000 CpGi (1k × 5-window) (10%)
- 1,250 planted-motif synthetic in genomic bg (2.5%)
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

MOTIFS = [
    "CCGCGTGGTGGCAG", "CCCTC", "GGGCGG", "TGACTCA", "TGAGTCA",
    "GGGACTTTCC", "GGGAATTTCC", "TATAAA", "TATATAA", "AGATAAG",
    "GATAAG", "CACGTG", "CAGCTG", "GGAAGT", "ACAGGAAGT",
    "TGTTTAC", "GTAAACA", "CCAAT", "ATTGCAT", "ATGCAAAT",
    "GGGGTGGGG", "TGTGGT", "GGAATG", "GCGCATGCGC", "CCATCTT",
    "AATTAAT", "TGCGTGGGCG", "TGACGTCA", "AGGTCA", "AGAACA",
    "CACCC", "TTCCGGAA", "AACCGGTT",
]

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

def sample_planted_motifs_genomic(rng, fa, n):
    """Generate n 200bp sequences with 1-3 TF motifs planted into
    RANDOM GENOMIC backgrounds."""
    lengths = {c: len(fa[c]) for c in CHROMS}
    weights = np.array([lengths[c] for c in CHROMS], dtype=float)
    weights /= weights.sum()
    seqs = []
    while len(seqs) < n:
        chrom = CHROMS[rng.choice(len(CHROMS), p=weights)]
        start = rng.integers(0, lengths[chrom] - L)
        bg = list(str(fa[chrom][start:start + L]).upper())
        if "N" in bg:
            continue
        # Plant 1-3 motifs (lower than exp 025 to preserve more context)
        n_motifs = int(rng.integers(1, 4))
        occupied = []
        for _ in range(n_motifs):
            motif = MOTIFS[int(rng.integers(0, len(MOTIFS)))]
            if rng.random() < 0.5:
                motif = revcomp(motif)
            mlen = len(motif)
            for _ in range(10):
                pos = int(rng.integers(0, L - mlen + 1))
                end = pos + mlen
                if not any(s < end and pos < e for s, e in occupied):
                    for j, b in enumerate(motif):
                        bg[pos + j] = b
                    occupied.append((pos, end))
                    break
        if rng.random() < 0.5:
            seq = revcomp("".join(bg))
        else:
            seq = "".join(bg)
        seqs.append(seq)
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
    a = sample_random_genomic(rng, fa, 21250); print(f"genomic: {len(a)}")
    b = sample_ccre_multiwindow(rng, fa, 4000); print(f"cCRE 5x-windowed: {len(b)}")
    c = sample_cpgi_multiwindow(rng, fa, 1000); print(f"CpGi 5x-windowed: {len(c)}")
    d = sample_planted_motifs_genomic(rng, fa, 1250); print(f"planted motifs (genomic bg): {len(d)}")
    e = sample_uniform_random(rng, 1250); print(f"uniform: {len(e)}")
    f = sample_mono_shuffled_ccre(rng, fa, 1250); print(f"mono-shuf: {len(f)}")
    combined = a + b + c + d + e + f
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
