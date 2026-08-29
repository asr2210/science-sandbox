"""016_ccre_plus_ctspecific: 40k cCREs + 10k high-cross-CT-std Malinois.

Exp 015 showed CT-specific Malinois sequences boost eval_04 by +0.03 but
cost −0.03 on eval_01 (distribution mismatch from pure CT-specific
selection). Hypothesis: a small CT-specific minority (10k) on top of a
cCRE base (40k) should preserve eval_01 (the cCRE base dominates) while
still contributing CT-discrimination signal that helps eval_04.

This is the "main course + spice" framing: cCRE is the bulk training
distribution (which controls eval_01), and Malinois CT-specific
sequences add labeled cross-CT contrast.

Generalization rationale: cell-type discriminator motifs are useful for
any cell-type-specific prediction task. Even on unseen cell types,
knowing which TF motifs distinguish K562 vs HepG2 helps the model
factor sequence → activity along TF-family axes that recur across
unseen tissues.
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
N_CCRE = 40000
N_MPRA = 10000
RNG_SEED = 16

QUOTA = {
    "PLS":        4500,
    "pELS":       5500,
    "dELS":       8500,
    "TF":         5000,
    "CA":         5000,
    "CA-CTCF":    4500,
    "CA-H3K4me3": 4000,
    "CA-TF":      3000,
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


def load_malinois_ctspecific(path, n_top):
    seqs = []; spec = []
    with open(path) as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            s = parts[11]
            if len(s) != L:
                continue
            if any(c not in "ACGT" for c in s):
                continue
            try:
                k = float(parts[5]); h = float(parts[6]); n = float(parts[7])
            except ValueError:
                continue
            arr = np.array([k, h, n])
            spec.append(arr.std())
            seqs.append(s)
    spec = np.array(spec)
    top_idx = np.argpartition(-spec, n_top)[:n_top]
    return [seqs[i] for i in top_idx]


def main():
    keep = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    chroms = load_hg38(HG38_FA_GZ, keep)
    by_type = load_ccres(CCRE_BED, set(chroms.keys()))

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

    mpra_picks = load_malinois_ctspecific(MPRA_PATH, N_MPRA)
    seqs.extend(mpra_picks)
    print(f"  malinois CT-specific added: {len(mpra_picks)}", flush=True)

    assert len(seqs) == N_CCRE + N_MPRA, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
