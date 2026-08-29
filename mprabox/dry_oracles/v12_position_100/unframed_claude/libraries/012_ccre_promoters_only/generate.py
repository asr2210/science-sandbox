"""Exp 012: ENCODE cCRE V4 PROMOTERS only.

Promoters are the most consistently active regulatory class. 47k Promoter +
Proximal-enhancer cCREs (high-activity classes) pad to 50k. 200bp windows
centered on cCRE midpoints. Tests whether HIGH-ACTIVITY bias matters.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
SEED = 43

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()

promoters = []
proxenh = []
with open(os.path.join(DATA, "encodeCcre.bed")) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 10:
            continue
        chrom = parts[0]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(parts[1]), int(parts[2])
        except ValueError:
            continue
        center = (s + e) // 2
        cls = parts[9]
        if cls == "Promoter":
            promoters.append((chrom, center))
        elif cls == "Proximal enhancer":
            proxenh.append((chrom, center))
print(f"Promoters: {len(promoters)}, Proximal enhancers: {len(proxenh)}")

acgt = set("ACGT")
rng = np.random.default_rng(SEED)

def extract(items, want):
    rng.shuffle(items)
    out = []
    for chrom, center in items:
        seq = CHRS[chrom]
        s = center - HALF
        if s < 0 or s + L > len(seq):
            continue
        w = seq[s:s + L]
        if set(w) <= acgt:
            out.append(w)
        if len(out) >= want:
            break
    return out

prom_seqs = extract(promoters, len(promoters))
pad_n = N - len(prom_seqs)
extra = extract(proxenh, pad_n) if pad_n > 0 else []
print(f"got {len(prom_seqs)} promoter seqs + {len(extra)} proximal enh seqs")
seqs = prom_seqs + extra
if len(seqs) < N:
    # safety pad with random genome
    chr_keys = list(CHRS.keys())
    weights = np.array([len(CHRS[k]) for k in chr_keys], dtype=np.float64)
    weights /= weights.sum()
    while len(seqs) < N:
        ck = chr_keys[rng.choice(len(chr_keys), p=weights)]
        c = CHRS[ck]
        s = rng.integers(0, len(c) - L + 1)
        w = c[s:s + L]
        if set(w) <= acgt:
            seqs.append(w)
seqs = seqs[:N]
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
