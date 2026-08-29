"""Exp 011: k-mer topic-style cluster library.

Cluster a large pool of DHS+cCRE sequences by 4-mer composition into 50
clusters via minibatch k-means; sample 1000 sequences per cluster to build
a 50k library that explicitly covers every k-mer cluster.

Proxy for LDA topic modeling — tests the 'dhs_topic' hypothesis.
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
N_CLUSTERS = 50
PER_CLUSTER = N // N_CLUSTERS  # 1000
POOL_SIZE = 250_000
SEED = 41

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

# Build a large pool of regulatory 200bp windows from cCREs.
pool_seqs = []
acgt = set("ACGT")
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
        start = center - HALF
        end = start + L
        if start < 0 or end > len(CHRS[chrom]):
            continue
        w = CHRS[chrom][start:end]
        if set(w) <= acgt:
            pool_seqs.append(w)
print(f"cCRE pool: {len(pool_seqs)}")

# Shuffle and cap to POOL_SIZE.
rng = np.random.default_rng(SEED)
rng.shuffle(pool_seqs)
pool_seqs = pool_seqs[:POOL_SIZE]
print(f"using pool of {len(pool_seqs)}")

# Compute 4-mer counts per sequence.
K = 4
N_KMERS = 4 ** K  # 256
print("computing 4-mer features...")
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq: str) -> np.ndarray:
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

X = np.stack([kmer_vec(s) for s in pool_seqs])
print(f"feature matrix: {X.shape}")

# MiniBatch k-means with 50 clusters.
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=4096, n_init=3, max_iter=200)
labels = km.fit_predict(X)
print("cluster sizes:", np.bincount(labels, minlength=N_CLUSTERS))

# Sample PER_CLUSTER seqs per cluster.
final = []
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) >= PER_CLUSTER:
        chosen = rng.choice(members, size=PER_CLUSTER, replace=False)
    else:
        chosen = rng.choice(members, size=PER_CLUSTER, replace=True)
    for i in chosen:
        final.append(pool_seqs[i])

assert len(final) == N
rng.shuffle(final)
with open(OUT, "w") as f:
    f.write("\n".join(final) + "\n")
print(f"wrote {OUT}: {N} x {L}")
