"""Exp 019: hybrid union of multiple cCRE strategies.

10k each from 5 different selection rationales (deduplicated):
  A) topic-stratified (4-mer K-Means(50))
  B) TFBS-hub (top by TFBS-cluster overlap count)
  C) DHS-summit centered (multi-cell K562+HepG2+SKNSH)
  D) Promoter cCREs (highest activity class)
  E) Random cCREs (no selection bias — control)

Hypothesis: each rationale captures slightly different regulatory features.
Union should give the model more comprehensive coverage.
"""
import os
import gzip
import glob
import numpy as np
from sklearn.cluster import MiniBatchKMeans

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
SEED = 89
PER_GROUP = 10_000

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

acgt = set("ACGT")

# Load all cCREs once with class label (column 9 of bed9+ is V4 class)
ccres = []  # (chrom, center, class)
with open(os.path.join(DATA, "encodeCcre.bed")) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom = parts[0]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        cls = parts[9] if len(parts) > 9 else ""
        ccres.append((chrom, (s + e) // 2, cls))
print(f"cCREs loaded: {len(ccres)}")

def get_window(chrom, center):
    start = center - HALF
    end = start + L
    if start < 0 or end > len(CHRS[chrom]):
        return None
    w = CHRS[chrom][start:end]
    if not (set(w) <= acgt):
        return None
    return w

# Materialize all valid cCRE windows once.
all_valid = []  # (chrom, center, cls, seq)
for chrom, center, cls in ccres:
    w = get_window(chrom, center)
    if w is not None:
        all_valid.append((chrom, center, cls, w))
print(f"valid cCRE windows: {len(all_valid)}")

rng = np.random.default_rng(SEED)
selected = {}  # seq -> True

def add_unique(seqs, want, source):
    n_added = 0
    for s in seqs:
        if s in selected:
            continue
        selected[s] = True
        n_added += 1
        if n_added >= want:
            break
    print(f"  {source}: added {n_added}/{want}")
    return n_added

# A) topic-stratified: 4-mer K-Means(50) over a random 200k subsample.
print("Group A: topic-stratified...")
K = 4
N_KMERS = 4 ** K
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq):
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

idx_perm = rng.permutation(len(all_valid))[:200_000]
subsample = [all_valid[i] for i in idx_perm]
Xa = np.stack([kmer_vec(s[3]) for s in subsample])
km = MiniBatchKMeans(n_clusters=50, random_state=SEED, batch_size=4096, n_init=2, max_iter=150)
labels = km.fit_predict(Xa)
group_a_seqs = []
for c in range(50):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(200, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    for i in chosen:
        group_a_seqs.append(subsample[i][3])
rng.shuffle(group_a_seqs)
add_unique(group_a_seqs, PER_GROUP, "A topic")

# B) TFBS-hub
print("Group B: TFBS-hub...")
tfbs_by_chrom = {}
with gzip.open(os.path.join(DATA, "encRegTfbsClusteredWithCells.hg38.bed.gz"), "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        chrom = parts[0]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        tfbs_by_chrom.setdefault(chrom, []).append((s + e) // 2)
for c in tfbs_by_chrom:
    tfbs_by_chrom[c] = np.array(sorted(tfbs_by_chrom[c]))

counts = np.empty(len(all_valid), dtype=np.int32)
for i, (chrom, center, _, _) in enumerate(all_valid):
    arr = tfbs_by_chrom.get(chrom)
    if arr is None:
        counts[i] = 0
    else:
        start = center - HALF
        end = start + L
        lo = np.searchsorted(arr, start)
        hi = np.searchsorted(arr, end)
        counts[i] = hi - lo
jitter = rng.random(len(all_valid))
order_b = np.lexsort((jitter, -counts))
group_b_seqs = [all_valid[i][3] for i in order_b[:30_000]]
add_unique(group_b_seqs, PER_GROUP, "B TFBS-hub")

# C) DHS-summit centered
print("Group C: multi-cell DHS summits...")
dhs_summits = []
for bed in sorted(glob.glob(os.path.join(DATA, "k562_*.bed.gz")) +
                  glob.glob(os.path.join(DATA, "hepg2_*.bed.gz")) +
                  glob.glob(os.path.join(DATA, "sknsh_*.bed.gz"))):
    with gzip.open(bed, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 10:
                continue
            chrom = parts[0]
            if chrom not in CHRS:
                continue
            try:
                s, e = int(parts[1]), int(parts[2])
                offset = int(parts[9])
                summit = s + offset if offset >= 0 else (s + e) // 2
                signal = float(parts[6])
            except (ValueError, IndexError):
                continue
            dhs_summits.append((chrom, summit, signal))
# top by signal
dhs_summits.sort(key=lambda x: -x[2])
group_c_seqs = []
seen = set()
for chrom, pos, _ in dhs_summits:
    key = (chrom, pos // 100)
    if key in seen:
        continue
    seen.add(key)
    w = get_window(chrom, pos)
    if w is not None:
        group_c_seqs.append(w)
    if len(group_c_seqs) >= 30_000:
        break
add_unique(group_c_seqs, PER_GROUP, "C DHS-summit")

# D) Promoter cCREs
print("Group D: promoter cCREs...")
promoters = [v[3] for v in all_valid if "Promoter" in v[2] or "TSS" in v[2]]
rng.shuffle(promoters)
add_unique(promoters, PER_GROUP, "D promoter")

# E) Random cCREs
print("Group E: random cCREs...")
random_idx = rng.permutation(len(all_valid))[:30_000]
group_e_seqs = [all_valid[i][3] for i in random_idx]
add_unique(group_e_seqs, PER_GROUP, "E random")

# Fill any shortfall from random cCREs.
final = list(selected.keys())
if len(final) < N:
    print(f"shortfall: {N - len(final)} - filling random")
    extra = rng.permutation(len(all_valid))
    for i in extra:
        s = all_valid[i][3]
        if s in selected:
            continue
        selected[s] = True
        final.append(s)
        if len(final) >= N:
            break
final = final[:N]
rng.shuffle(final)
print(f"final: {len(final)}")

with open(OUT, "w") as f:
    f.write("\n".join(final) + "\n")
print(f"wrote {OUT}: {N} x {L}")
