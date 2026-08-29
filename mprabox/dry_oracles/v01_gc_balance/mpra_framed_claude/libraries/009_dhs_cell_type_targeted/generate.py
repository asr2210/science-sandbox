"""009_dhs_cell_type_targeted: 50k DHS sites from K562/HepG2/SKNSH-relevant components.

Per DHS-index tissue-component groupings:
  K562 ~ Myeloid/erythroid + Lymphoid
  HepG2 ~ Cancer/epithelial + Digestive
  SK-N-SH ~ Neural
  + Tissue invariant (housekeeping, cross-cell-type)

Equal 12.5k from each of these 4 pools = 50k total. Within each pool,
sampling prob ∝ log(1+numsamples) so broader/more-reproducible elements
preferred.

Hypothesis: targeting DHS to the components matching the eval cell types
should beat exp 007 (16-component uniform stratification) and may approach
or beat exp 002 (cCRE) because cell-type-matched data carries the most
signal for those specific cell types' activity.

Generalization caveat: this library is *tuned* to the three labeled cell
types. It would be expected to under-perform on unseen-cell-type evals
that need other tissue grammar. We're using the eval suite (which is
labeled cell-type-centric) as a guide while accepting that the gain may
not transfer to unmeasured cell types. We will test this hypothesis later
with a more cross-tissue library.
"""
import gzip
import os
from collections import defaultdict

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
HG38_FA_GZ = f"{ROOT}/data/hg38/hg38.fa.gz"
DHS_PATH = f"{ROOT}/data/dhs/DHS_Index.txt.gz"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 9

POOLS = {
    "K562": ["Myeloid / erythroid", "Lymphoid"],
    "HepG2": ["Cancer / epithelial", "Digestive"],
    "SKNSH": ["Neural"],
    "INV":   ["Tissue invariant"],
}


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


def load_dhs_by_component(path, keep, components_needed):
    by_comp = defaultdict(list)
    with gzip.open(path, "rt") as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in keep:
                continue
            comp = parts[9]
            if comp not in components_needed:
                continue
            by_comp[comp].append((parts[0], int(parts[6]), int(parts[5])))
    return by_comp


def extract(seq, mid, length):
    half = length // 2
    s = mid - half; e = s + length
    if s < 0 or e > len(seq):
        return None
    win = seq[s:e]
    if "N" in win:
        return None
    return win


def main():
    keep = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    needed_comps = set()
    for comps in POOLS.values():
        needed_comps.update(comps)
    print("Loading hg38...", flush=True)
    chroms = load_hg38(HG38_FA_GZ, keep)
    print("Loading DHS (filtered components)...", flush=True)
    by_comp = load_dhs_by_component(DHS_PATH, set(chroms.keys()), needed_comps)
    for k, v in by_comp.items():
        print(f"  {k:30s} {len(v):>8d}", flush=True)

    rng = np.random.default_rng(RNG_SEED)
    seqs = []
    per_pool = N // len(POOLS)
    for pool_name, comps in POOLS.items():
        merged = []
        for c in comps:
            merged.extend(by_comp[c])
        ns = np.array([m[2] for m in merged], dtype=np.float64)
        weights = np.log1p(ns)
        weights = weights / weights.sum()
        n_try = min(len(merged), per_pool * 3)
        idx_pool = rng.choice(len(merged), size=n_try, replace=False, p=weights)
        added = 0
        for idx in idx_pool:
            if added >= per_pool:
                break
            chrom, summit, _ = merged[idx]
            win = extract(chroms[chrom], summit, L)
            if win is None:
                continue
            seqs.append(win)
            added += 1
        print(f"  pool {pool_name}: {added}/{per_pool}", flush=True)

    assert len(seqs) == N, f"got {len(seqs)}"
    rng.shuffle(seqs)
    with open(OUT_PATH, "w") as f:
        for s in seqs:
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
