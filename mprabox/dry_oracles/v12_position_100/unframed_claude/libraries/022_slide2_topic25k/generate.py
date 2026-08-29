"""Exp 022: 2 sliding windows x 25k topic-stratified cCREs.

Combines 020's sliding-window trick with 011's topic clustering for diversity:
- 25k unique cCREs selected via 4-mer K-Means(50) topic stratification from
  a 250k cCRE subsample (proven 011 recipe for diversity)
- For each, extract 2 windows at offsets {-50, +50} from cCRE center
- Total 50k unique seqs

Hypothesis: combines diversity (topic) with augmentation (slide), should
beat either alone.
"""
import os
import numpy as np
from sklearn.cluster import MiniBatchKMeans

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
N_UNIQUE = 25_000
OFFSETS = [-50, 50]
N_CLUSTERS = 50
PER_CLUSTER = N_UNIQUE // N_CLUSTERS  # 500
POOL_SIZE = 250_000
SEED = 107

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

acgt = set("ACGT")
outer_half = HALF + max(abs(o) for o in OFFSETS)
# Pool: cCREs whose centers have enough surrounding context to extract both windows.
ccre_centers = []  # (chrom, center)
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
        ccre_centers.append((chrom, center))
print(f"valid cCRE centers: {len(ccre_centers)}")

rng = np.random.default_rng(SEED)
# Subsample to POOL_SIZE
perm = rng.permutation(len(ccre_centers))[:POOL_SIZE]
pool = [ccre_centers[i] for i in perm]
# Reference window for feature extraction (center)
pool_seqs = [CHRS[c][p - HALF:p + HALF] for c, p in pool]
print(f"pool: {len(pool_seqs)}")

K = 4
N_KMERS = 4 ** K
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq):
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

X = np.stack([kmer_vec(s) for s in pool_seqs])
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=4096, n_init=3, max_iter=200)
labels = km.fit_predict(X)
sizes = np.bincount(labels, minlength=N_CLUSTERS)
print(f"cluster sizes: min={sizes.min()} max={sizes.max()}")

selected_idx = []
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(PER_CLUSTER, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    selected_idx.extend(chosen.tolist())
# Fill from remaining
if len(selected_idx) < N_UNIQUE:
    remaining = N_UNIQUE - len(selected_idx)
    mask = np.ones(len(pool), dtype=bool)
    mask[selected_idx] = False
    rem = np.arange(len(pool))[mask]
    fill = rng.choice(rem, size=remaining, replace=False)
    selected_idx.extend(fill.tolist())
selected_idx = selected_idx[:N_UNIQUE]
print(f"selected {len(selected_idx)} unique cCREs")

# Generate 2 windows per cCRE.
seqs = []
for si in selected_idx:
    chrom, center = pool[si]
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
