"""Exp 028: TFBS-top + topic cluster within + 4 slides.

Pipeline:
1) Take top 50_000 cCREs by TFBS density (in 400bp context).
2) Topic-cluster (4-mer K-Means(50)) those 50_000 to 50 clusters.
3) From each cluster, take 250 cCREs (balanced).
4) For each chosen cCRE, extract 4 sliding windows {-75,-25,25,75}.
5) Result: 50 * 250 * 4 = 50_000.

Hypothesis: top-TFBS adds info density; topic cluster within ensures diversity;
slide aug expands views. Combines all three best ideas.
"""
import os
import gzip
import numpy as np
from sklearn.cluster import MiniBatchKMeans

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
TOP_TFBS = 50_000
N_CLUSTERS = 50
PER_CLUSTER = 250
OFFSETS = [-75, -25, 25, 75]
SEED = 181

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

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

acgt = set("ACGT")
outer_half = HALF + max(abs(o) for o in OFFSETS)
candidates = []
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
        center = (s + e) // 2
        if center - outer_half < 0 or center + outer_half > len(CHRS[chrom]):
            continue
        ctx = CHRS[chrom][center - outer_half:center + outer_half]
        if not (set(ctx) <= acgt):
            continue
        arr = tfbs_by_chrom.get(chrom)
        if arr is None:
            count = 0
        else:
            lo = np.searchsorted(arr, center - outer_half)
            hi = np.searchsorted(arr, center + outer_half)
            count = hi - lo
        candidates.append((chrom, center, count))
print(f"candidates: {len(candidates)}")

rng = np.random.default_rng(SEED)
counts = np.array([c[2] for c in candidates], dtype=np.int32)
jitter = rng.random(len(candidates))
order = np.lexsort((jitter, -counts))
top = order[:TOP_TFBS]
print(f"top TFBS counts: max={counts[top[0]]} median={int(np.median(counts[top]))} min={counts[top[-1]]}")

# Topic cluster the top-TFBS subset by 4-mer
K = 4
N_KMERS = 4 ** K
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3
def kmer_vec(seq):
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

print("computing 4-mer features for top-TFBS subset...")
top_seqs = [CHRS[candidates[i][0]][candidates[i][1] - HALF:candidates[i][1] + HALF] for i in top]
X = np.stack([kmer_vec(s) for s in top_seqs])
print(f"feature matrix: {X.shape}")

print("clustering...")
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=4096, n_init=2, max_iter=150)
labels = km.fit_predict(X)
sizes = np.bincount(labels, minlength=N_CLUSTERS)
print(f"cluster sizes: min={sizes.min()} max={sizes.max()}")

# Sample PER_CLUSTER per cluster
chosen_top_idx = []
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(PER_CLUSTER, len(members))
    pick = rng.choice(members, size=take, replace=False)
    chosen_top_idx.extend(pick.tolist())
# Fill from remaining top-TFBS
if len(chosen_top_idx) < 12_500:
    remaining = 12_500 - len(chosen_top_idx)
    mask = np.ones(len(top), dtype=bool)
    mask[chosen_top_idx] = False
    rem = np.arange(len(top))[mask]
    fill = rng.choice(rem, size=remaining, replace=False)
    chosen_top_idx.extend(fill.tolist())
chosen_top_idx = chosen_top_idx[:12_500]
print(f"selected {len(chosen_top_idx)} cCREs")

seqs = []
for cti in chosen_top_idx:
    cand_i = top[cti]
    chrom, center, _ = candidates[cand_i]
    for off in OFFSETS:
        start = center + off - HALF
        end = start + L
        seqs.append(CHRS[chrom][start:end])
assert len(seqs) == N
print(f"unique seqs: {len(set(seqs))} / {len(seqs)}")
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
