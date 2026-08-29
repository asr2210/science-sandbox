"""Exp 018: reverse-complement augmentation.

25k unique cCRE windows (4-mer topic-stratified) + 25k their reverse complements.
Hypothesis: most CNN models aren't strand-symmetric; RC of a cCRE has same
regulatory activity but different sequence. Adding both teaches the model
that RC-equivalent sequences have similar activity — should improve generalization
to held-out evals that may sample either strand.
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
N_CLUSTERS = 50
PER_CLUSTER = N_UNIQUE // N_CLUSTERS  # 500
POOL_SIZE = 250_000
SEED = 83

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

def kmer_vec(seq):
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    idx = arr[:-K+1] * (4**(K-1)) + arr[1:-K+2] * (4**(K-2)) + arr[2:-K+3] * (4**(K-3)) + arr[3:]
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

print("computing 4-mer features...")
X = np.stack([kmer_vec(s) for s in pool_seqs])

km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=4096, n_init=3, max_iter=200)
labels = km.fit_predict(X)

unique_idx = []
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(PER_CLUSTER, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    unique_idx.extend(chosen.tolist())
# Fill from remaining
if len(unique_idx) < N_UNIQUE:
    remaining = N_UNIQUE - len(unique_idx)
    mask = np.ones(len(pool_seqs), dtype=bool)
    mask[unique_idx] = False
    pool = np.arange(len(pool_seqs))[mask]
    fill = rng.choice(pool, size=remaining, replace=False)
    unique_idx.extend(fill.tolist())
unique_idx = unique_idx[:N_UNIQUE]
unique_seqs = [pool_seqs[i] for i in unique_idx]
print(f"unique cCREs: {len(unique_seqs)}")

_COMP = str.maketrans("ACGT", "TGCA")
def revcomp(s):
    return s.translate(_COMP)[::-1]

rc_seqs = [revcomp(s) for s in unique_seqs]
all_seqs = unique_seqs + rc_seqs
assert len(all_seqs) == N
rng.shuffle(all_seqs)
with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
