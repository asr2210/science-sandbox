"""Exp 009: ENCODE cCRE V4 class-stratified 200bp library.

The 2.35M cCRE V4 elements are classified into 8 regulatory classes
(Promoter, Proximal/Distal enhancer, CTCF, CA, CA-CTCF, CA-TF, CA-H3K4me3, TF).
Sample ~6250 per class, center 200bp on the cCRE midpoint. This tests the
'dhs_topic' style hypothesis: explicit regulatory CATEGORY diversity helps.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
HALF = L // 2
SEED = 31

CHRS = {}
for n in list(range(1, 23)) + ["X"]:
    name = f"chr{n}"
    with open(os.path.join(DATA, f"{name}.fa")) as f:
        f.readline()
        CHRS[name] = "".join(line.strip() for line in f).upper()
print("loaded", len(CHRS), "chromosomes")

# Group cCREs by class.
by_class = {}
with open(os.path.join(DATA, "encodeCcre.bed")) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 10:
            continue
        chrom, start, end, _id, _, _, _, _, _, cls = parts[:10]
        if chrom not in CHRS:
            continue
        try:
            s, e = int(start), int(end)
        except ValueError:
            continue
        center = (s + e) // 2
        by_class.setdefault(cls, []).append((chrom, center))
for cls, lst in sorted(by_class.items()):
    print(f"  {cls}: {len(lst)}")

rng = np.random.default_rng(SEED)
acgt = set("ACGT")
per_class = N // len(by_class)
extras = N - per_class * len(by_class)
seqs = []
for i, (cls, lst) in enumerate(sorted(by_class.items())):
    target = per_class + (1 if i < extras else 0)
    idx = rng.permutation(len(lst))
    got = 0
    for j in idx:
        chrom, center = lst[j]
        seq = CHRS[chrom]
        s = center - HALF
        if s < 0 or s + L > len(seq):
            continue
        w = seq[s:s + L]
        if set(w) <= acgt:
            seqs.append(w)
            got += 1
        if got >= target:
            break
    print(f"  {cls}: got {got}")

# Fill if any class came up short.
if len(seqs) < N:
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

rng.shuffle(seqs)
seqs = seqs[:N]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
