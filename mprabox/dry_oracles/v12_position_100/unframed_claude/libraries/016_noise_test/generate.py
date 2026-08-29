"""Exp 016: noise-floor measurement.

Rerun exp 011's exact recipe (4-mer K-Means(50) on 250k cCRE subsample, 1000/cluster)
with a different seed. If eval_01 is ~0.076 ± 0.005 then 011's lift is real;
if it bounces ±0.015 the recent deltas (014-015) are within noise.
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
N_CLUSTERS = 50
PER_CLUSTER = N // N_CLUSTERS  # 1000
POOL_SIZE = 250_000
SEED = 911

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

rng = np.random.default_rng(SEED)
rng.shuffle(pool_seqs)
pool_seqs = pool_seqs[:POOL_SIZE]

K = 4
N_KMERS = 4 ** K
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq: str) -> np.ndarray:
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

X = np.stack([kmer_vec(s) for s in pool_seqs])
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=4096, n_init=3, max_iter=200)
labels = km.fit_predict(X)

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
