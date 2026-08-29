"""Exp 014: 4-mer K-Means(80) on FULL cCRE pool, no replacement.

Improvement over 011:
- Use ALL 2.35M cCREs as the candidate pool (vs 250k subsample).
- 80 clusters (vs 50).
- Sample at most cluster_size per cluster, NEVER with replacement.
- Fill the residual with stratified randomly chosen overall.
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
N_CLUSTERS = 80
PER_CLUSTER = N // N_CLUSTERS  # 625
SEED = 53
K = 4
N_KMERS = 4 ** K

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

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

_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq: str) -> np.ndarray:
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    powers = [4**(K-1-i) for i in range(K)]
    idx = sum(arr[i:len(arr) - K + 1 + i] * powers[i] for i in range(K))
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

print("computing 4-mer features for full pool...")
X = np.empty((len(pool_seqs), N_KMERS), dtype=np.float32)
for i, s in enumerate(pool_seqs):
    X[i] = kmer_vec(s)
print(f"X.shape={X.shape}, dtype={X.dtype}")

print("running MiniBatchKMeans...")
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=8192, n_init=2, max_iter=150)
labels = km.fit_predict(X)
sizes = np.bincount(labels, minlength=N_CLUSTERS)
print("cluster sizes:", sorted(sizes.tolist()))

rng = np.random.default_rng(SEED)
selected_idx = []
# First pass: balanced sampling at most PER_CLUSTER (no replacement).
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(PER_CLUSTER, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    selected_idx.extend(chosen.tolist())

# Residual: fill to N from remaining sequences (sample without replacement).
remaining = N - len(selected_idx)
if remaining > 0:
    all_idx = np.arange(len(pool_seqs))
    mask = np.ones(len(pool_seqs), dtype=bool)
    mask[selected_idx] = False
    pool = all_idx[mask]
    fill = rng.choice(pool, size=remaining, replace=False)
    selected_idx.extend(fill.tolist())

print(f"selected {len(selected_idx)} (unique={len(set(selected_idx))})")
selected_idx = selected_idx[:N]
rng.shuffle(selected_idx)
seqs = [pool_seqs[i] for i in selected_idx]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
