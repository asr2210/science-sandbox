"""014_ccre_malinois_mix: 25k stratified cCREs + 25k random Malinois oligos.

Random cCREs (exp 002) gave 0.6921; random Malinois (exp 012) gave 0.6856.
They're nearly equivalent at the eval, but they're qualitatively different
data:
  - cCREs: epigenetically defined regulatory elements, centered on
    biochemical signatures (DNase + CTCF/H3K4me3 / TF binding).
  - Malinois: 200bp windows centered on GWAS/eQTL variants, sampling
    from regions associated with variation but not necessarily with
    strong canonical regulatory marks.

If the two sources expose the model to complementary motif arrangements
that don't overlap, the union should beat either alone. If they cover
the same regulatory grammar (just with different filters), the mix
should be ~ tied.

Generalization rationale: mixing two independently-curated regulatory
data sources is a cheap way to broaden the training distribution of
motif arrangements without giving up the "real-biological-sequence"
prior. If the model is currently saturating on the cCRE motif diversity,
Malinois variant windows might add residual signal.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
CCRE_BED = f"{ROOT}/data/encode/GRCh38-cCREs.bed"
MPRA_PATH = f"{ROOT}/data/mpra/malinois_mpra.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N_CCRE = 25000
N_MPRA = 25000
RNG_SEED = 14

# Halved quotas from exp 002 (which was 50k); now sums to 25k
QUOTA = {
    "PLS":        3000,
    "pELS":       3500,
    "dELS":       5000,
    "TF":         3000,
    "CA":         3000,
    "CA-CTCF":    3000,
    "CA-H3K4me3": 2500,
    "CA-TF":      2000,
}
assert sum(QUOTA.values()) == N_CCRE


def load_hg38(path, keep):
    chroms = {}; cur = None; chunks = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if cur and cur in keep:
                    chroms[cur] = "".join(chunks).upper()
                cur = line[1:].split()[0]; chunks = []
            elif cur in keep:
                chunks.append(line.rstrip())
        if cur in keep:
            chroms[cur] = "".join(chunks).upper()
    return chroms


def load_ccres(path, keep):
    by_type = defaultdict(list)
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            by_type[parts[9]].append((parts[0], int(parts[1]), int(parts[2])))
    return by_type


def extract(seq, mid, length):
    half = length // 2
    s = mid - half; e = s + length
    if s < 0 or e > len(seq):
        return None
    win = seq[s:e]
    if "N" in win:
        return None
    return win


def load_malinois(path):
    seqs = []
    with open(path) as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            s = parts[11]
            if len(s) != L:
                continue
            if any(c not in "ACGT" for c in s):
                continue
            seqs.append(s)
    return seqs


def main():
    keep = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    chroms = load_hg38(HG38_FA_GZ, keep)
    by_type = load_ccres(CCRE_BED, set(chroms.keys()))
    mpra = load_malinois(MPRA_PATH)
    print(f"  malinois 200bp pool: {len(mpra)}", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []
    for ctype, quota in QUOTA.items():
        pool = by_type[ctype]
        order = rng.permutation(len(pool))
        added = 0
        for idx in order:
            if added >= quota:
                break
            chrom, start, end = pool[idx]
            win = extract(chroms[chrom], (start + end) // 2, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  cCRE {ctype}: {added}/{quota}", flush=True)

    idx = rng.choice(len(mpra), size=N_MPRA, replace=False)
    seqs.extend(mpra[i] for i in idx)
    print(f"  malinois added: {N_MPRA}", flush=True)

    assert len(seqs) == N_CCRE + N_MPRA, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
