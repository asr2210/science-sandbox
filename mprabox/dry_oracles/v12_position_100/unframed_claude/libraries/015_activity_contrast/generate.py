"""Exp 015: explicit activity contrast.

Build a library that gives the model strong positive AND negative examples:
- 25k POSITIVE: union of K562/HepG2/SKNSH DHS peaks, kept by stratified
  4-mer topic cluster (50 clusters, 500 per cluster) to also cover diversity.
- 25k NEGATIVE: intergenic 200bp windows with NO cCRE within +-50kb
  (true regulatory deserts; the model needs negative anchors to learn
  rank order).

Theory: Pearson cares about rank order. Random + cCRE topic libraries
only cover the "kinda active" end of the activity axis. Contrast with
true silent intergenic should pull the dynamic range up.
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
N_POS = 25_000
N_NEG = 25_000
N_CLUSTERS = 50
PER_CLUSTER = N_POS // N_CLUSTERS  # 500
SEED = 59
DESERT_RADIUS = 10_000
K = 4
N_KMERS = 4 ** K

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded chrs")

# --- POSITIVES: collect all DHS summits across K562/HepG2/SKNSH ---
dhs_summits = []  # (chrom, summit_pos, score)
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
                signal = float(parts[6])
                offset = int(parts[9])  # narrowPeak summit
                summit = s + offset if offset >= 0 else (s + e) // 2
            except (ValueError, IndexError):
                continue
            dhs_summits.append((chrom, summit, signal))
print(f"DHS summits: {len(dhs_summits)}")

# Dedup by chrom/summit within 50bp
dhs_summits.sort()
dedup = []
last_chrom = None
last_pos = -10**9
for c, p, s in dhs_summits:
    if c == last_chrom and abs(p - last_pos) < 50:
        continue
    dedup.append((c, p, s))
    last_chrom = c
    last_pos = p
print(f"DHS summits after 50bp dedup: {len(dedup)}")

# Extract 200bp around each summit, ACGT-only
acgt = set("ACGT")
pos_pool = []
for c, p, _ in dedup:
    start = p - HALF
    end = start + L
    if start < 0 or end > len(CHRS[c]):
        continue
    w = CHRS[c][start:end]
    if set(w) <= acgt:
        pos_pool.append(w)
print(f"positive pool (post-filter): {len(pos_pool)}")

# Topic-cluster the positives for diversity
_TABLE = np.full(256, -1, dtype=np.int32)
_TABLE[ord("A")] = 0; _TABLE[ord("C")] = 1; _TABLE[ord("G")] = 2; _TABLE[ord("T")] = 3

def kmer_vec(seq: str) -> np.ndarray:
    arr = _TABLE[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]
    powers = [4**(K-1-i) for i in range(K)]
    idx = sum(arr[i:len(arr) - K + 1 + i] * powers[i] for i in range(K))
    vec = np.bincount(idx, minlength=N_KMERS).astype(np.float32)
    return vec / vec.sum()

print("computing 4-mer features for positives...")
Xp = np.empty((len(pos_pool), N_KMERS), dtype=np.float32)
for i, s in enumerate(pos_pool):
    Xp[i] = kmer_vec(s)

print("clustering positives...")
km = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=SEED, batch_size=8192, n_init=2, max_iter=150)
labels = km.fit_predict(Xp)
sizes = np.bincount(labels, minlength=N_CLUSTERS)
print(f"positive cluster sizes: min={sizes.min()} max={sizes.max()}")

rng = np.random.default_rng(SEED)
pos_idx = []
for c in range(N_CLUSTERS):
    members = np.where(labels == c)[0]
    if len(members) == 0:
        continue
    take = min(PER_CLUSTER, len(members))
    chosen = rng.choice(members, size=take, replace=False)
    pos_idx.extend(chosen.tolist())
# fill if short
if len(pos_idx) < N_POS:
    remaining = N_POS - len(pos_idx)
    mask = np.ones(len(pos_pool), dtype=bool)
    mask[pos_idx] = False
    pool = np.arange(len(pos_pool))[mask]
    fill = rng.choice(pool, size=remaining, replace=False)
    pos_idx.extend(fill.tolist())
pos_idx = pos_idx[:N_POS]
pos_seqs = [pos_pool[i] for i in pos_idx]
print(f"positives selected: {len(pos_seqs)}")

# --- NEGATIVES: intergenic windows >50kb from any cCRE ---
print("building cCRE position index by chrom for desert check...")
ccre_by_chrom = {}
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
        ccre_by_chrom.setdefault(chrom, []).append((s + e) // 2)
for c in ccre_by_chrom:
    ccre_by_chrom[c] = np.array(sorted(ccre_by_chrom[c]))
print(f"cCRE chrom counts: { {c: len(v) for c, v in ccre_by_chrom.items()} }")

neg_seqs = []
attempts = 0
chrom_list = list(CHRS.keys())
chrom_lens = np.array([len(CHRS[c]) for c in chrom_list], dtype=np.int64)
chrom_probs = chrom_lens / chrom_lens.sum()
while len(neg_seqs) < N_NEG and attempts < N_NEG * 50:
    attempts += 1
    ci = rng.choice(len(chrom_list), p=chrom_probs)
    chrom = chrom_list[ci]
    start = int(rng.integers(0, chrom_lens[ci] - L))
    end = start + L
    center = (start + end) // 2
    # nearest cCRE distance
    ccres = ccre_by_chrom.get(chrom)
    if ccres is None or len(ccres) == 0:
        nearest = 10**9
    else:
        i = np.searchsorted(ccres, center)
        cands = []
        if i < len(ccres):
            cands.append(abs(ccres[i] - center))
        if i > 0:
            cands.append(abs(center - ccres[i-1]))
        nearest = min(cands)
    if nearest < DESERT_RADIUS:
        continue
    w = CHRS[chrom][start:end]
    if set(w) <= acgt:
        neg_seqs.append(w)
print(f"negatives selected: {len(neg_seqs)} in {attempts} attempts")

assert len(pos_seqs) == N_POS
assert len(neg_seqs) == N_NEG
all_seqs = pos_seqs + neg_seqs
rng.shuffle(all_seqs)
with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {OUT}: {len(all_seqs)} x {L}")
