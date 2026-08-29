"""Experiment 018: DHS rare-component upweighting (013 principle on DHS).

Apply 013's rare-class upweighting principle to the Meuleman DHS Index.
- 009 quality filter: mean_signal >= q75 AND numsamples >= 5
- Group filtered sites by primary NMF component (16 cell-type vocabs)
- Sort components by post-filter pool size; smallest 8 = rare, largest 8 = abundant
- 8 rare × 5000 + 8 abundant × 1250 = 50000 (same 4:1 ratio as 013)
- 200bp centered on summit

Tests whether T8 (rare-class upweighting principle) generalizes from
cCRE classes to DHS NMF components.
"""
import gzip
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DHS = os.path.join(ROOT, "data", "DHS", "DHS_Index_hg38.txt.gz")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
SIG_QUANTILE = 0.75
MIN_SAMPLES = 5
RARE_PER = 5_000     # 8 rare components
ABUND_PER = 1_250    # 8 abundant components


def load_dhs_filtered_by_component():
    rows = []
    sigs = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in MAIN_CHROMS:
                continue
            sig = float(p[4])
            ns = int(p[5])
            summit = int(p[6])
            comp = p[9]
            rows.append((chrom, summit, sig, ns, comp))
            sigs.append(sig)
    sig_thresh = float(np.quantile(np.array(sigs), SIG_QUANTILE))
    by_comp = defaultdict(list)
    for chrom, summit, sig, ns, comp in rows:
        if sig >= sig_thresh and ns >= MIN_SAMPLES:
            by_comp[comp].append((chrom, summit))
    return by_comp, sig_thresh


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def assign_counts(by_comp):
    """Sort components by pool size; smallest 8 = rare, largest 8 = abundant."""
    sizes = sorted(by_comp.items(), key=lambda kv: len(kv[1]))
    counts = {}
    for i, (comp, pool) in enumerate(sizes):
        counts[comp] = RARE_PER if i < 8 else ABUND_PER
    assert sum(counts.values()) == N_SEQS, sum(counts.values())
    return counts


def generate(seed, by_comp, counts, tb):
    rng = np.random.default_rng(seed)
    out = []
    for comp, n_take in counts.items():
        pool = by_comp[comp]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, summit = pool[j]
            seq = extract(tb, chrom, summit, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{comp}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    print("loading + filtering DHS index by component...")
    by_comp, sig_thresh = load_dhs_filtered_by_component()
    print(f"  sig_thresh (q{SIG_QUANTILE})={sig_thresh:.3f}")
    counts = assign_counts(by_comp)
    for comp, pool in sorted(by_comp.items(), key=lambda kv: len(kv[1])):
        print(f"  {comp:30s}  pool={len(pool):>7,}  take={counts[comp]:>5,}")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_comp, counts, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
