"""Exp 007: maximally diverse mixed library.

50k = 10k from each of 5 sources:
- random_uniform
- dinuc Markov
- genome random windows
- K562 DHS centered (top by height)
- synthetic motif-dense

Tests whether library DIVERSITY (broad coverage of sequence regimes) helps.
"""
import os
import gzip
import glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
PER = N // 5
SEED = 23
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# -- 1. random_uniform
def gen_random():
    idx = rng.integers(0, 4, size=(PER, L), dtype=np.uint8)
    return ["".join(row) for row in bases[idx]]

# -- 2. dinuc Markov (genome-wide human dinuc freqs)
def gen_dinuc():
    dinuc = np.array([
        [0.097, 0.052, 0.072, 0.073],
        [0.073, 0.052, 0.010, 0.072],
        [0.060, 0.043, 0.052, 0.052],
        [0.063, 0.060, 0.073, 0.097],
    ], dtype=np.float64)
    trans = dinuc / dinuc.sum(axis=1, keepdims=True)
    marginal = dinuc.sum(axis=1) / dinuc.sum()
    cdf = np.cumsum(trans, axis=1)
    starts = rng.choice(4, size=PER, p=marginal)
    idx = np.empty((PER, L), dtype=np.uint8)
    idx[:, 0] = starts
    u = rng.random((PER, L - 1))
    for t in range(1, L):
        idx[:, t] = (u[:, t - 1, None] < cdf[idx[:, t - 1]]).argmax(axis=1)
    return ["".join(row) for row in bases[idx]]

# -- 3. genome random windows
def load_chr(name):
    with open(os.path.join(DATA, name)) as f:
        f.readline()
        return "".join(line.strip() for line in f).upper()

print("loading chromosomes...")
CHRS = {f"chr{n}": load_chr(f"chr{n}.fa") for n in list(range(1, 23)) + ["X"]}

def gen_genome():
    out = []
    chr_keys = list(CHRS.keys())
    weights = np.array([len(CHRS[k]) for k in chr_keys], dtype=np.float64)
    weights /= weights.sum()
    acgt = set("ACGT")
    while len(out) < PER:
        k = chr_keys[rng.choice(len(chr_keys), p=weights)]
        c = CHRS[k]
        s = rng.integers(0, len(c) - L + 1)
        w = c[s:s + L]
        if set(w) <= acgt:
            out.append(w)
    return out

# -- 4. K562 DHS centered, top by height
def gen_k562_dhs():
    best = {}
    for path in sorted(glob.glob(os.path.join(DATA, "k562_*.bed.gz"))):
        with gzip.open(path, "rt") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 8:
                    continue
                chrom = parts[0]
                try:
                    summit = int(parts[6])
                    height = float(parts[7])
                except ValueError:
                    continue
                if chrom not in CHRS:
                    continue
                k = (chrom, summit)
                if height > best.get(k, -1):
                    best[k] = height
    items = sorted(best.items(), key=lambda kv: -kv[1])
    acgt = set("ACGT")
    out = []
    for (chrom, summit), _ in items:
        seq = CHRS[chrom]
        s = summit - L // 2
        if s < 0 or s + L > len(seq):
            continue
        w = seq[s:s + L]
        if set(w) <= acgt:
            out.append(w)
        if len(out) >= PER:
            break
    return out

# -- 5. synthetic motif-dense
MOTIFS = [
    "TGACTCA", "GGGACTTTCC", "CCAAT", "TATAAA", "CCGCCC", "ATGCAAAT",
    "GATAA", "CACGTG", "GGGCGG", "AGGTCA", "TTGCGCAA", "TTCCGGAA",
    "AATAAA", "CCACCAGGTGGCAG", "GCCACGTGGC", "CAGCTG", "AGGAAG",
    "TGAGTCA", "GGGGAGGG", "TAATTA",
]
def gen_motif_dense():
    out = []
    for _ in range(PER):
        primary = MOTIFS[rng.integers(len(MOTIFS))]
        n_primary = 6 + int(rng.integers(0, 5))
        secondary = [MOTIFS[i] for i in rng.choice(len(MOTIFS), size=int(rng.integers(2, 5)), replace=False)]
        motifs_to_insert = [primary] * n_primary + secondary
        rng.shuffle(motifs_to_insert)
        while sum(len(m) for m in motifs_to_insert) + len(motifs_to_insert) + 1 > L and motifs_to_insert:
            motifs_to_insert.pop()
        spacer_total = L - sum(len(m) for m in motifs_to_insert)
        n = len(motifs_to_insert)
        breakpoints = sorted(rng.integers(0, spacer_total + 1, size=n))
        parts = []
        prev = 0
        for bp in breakpoints:
            parts.append(bp - prev)
            prev = bp
        parts.append(spacer_total - prev)
        pieces = []
        for sp_len, motif in zip(parts, motifs_to_insert):
            sp = "".join(bases[rng.integers(0, 4, size=sp_len)])
            pieces.append(sp); pieces.append(motif)
        pieces.append("".join(bases[rng.integers(0, 4, size=parts[-1])]))
        s = "".join(pieces); assert len(s) == L
        out.append(s)
    return out

seqs = gen_random() + gen_dinuc() + gen_genome() + gen_k562_dhs() + gen_motif_dense()
rng.shuffle(seqs)
assert len(seqs) == N, (len(seqs), N)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
