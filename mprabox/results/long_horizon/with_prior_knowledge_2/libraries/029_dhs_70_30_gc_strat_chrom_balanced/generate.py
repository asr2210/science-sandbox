"""Experiment 029 — dhs_70_30_gc_strat_chrom_balanced.

015's recipe with an added per-chromosome cap. Tests whether
balanced genomic coverage is an additional orthogonal axis to
(signal × numsamples × GC strat).

Recipe: same as 015 (35K signal-weighted + 15K numsamples-weighted,
both halves stratified across 5 equal-pop GC quintiles) BUT enforce
a hard per-chromosome cap during the draws.

Cap = ceil(50000 / 24 chroms * 1.2) = 2500 per chrom. The cap will
primarily bite chr1, chr2 (which have far more DHS than the global
mean); under-represented small chroms (chr21, chrY) will not hit
the cap and won't be inflated either — they're just unconstrained.
The effect is to TRIM over-represented chroms, redistributing draws
to mid-sized chroms.

Bins are processed in a shuffled order per seed, so the ordering
of cap-hits varies. If a bin can't fully fill due to cap exhaustion,
we'll see it in the per-bin counts.

Hypothesis: chromosomes with more DHS are more gene-dense regions
that may carry idiosyncratic regulatory grammar. Capping them might
encourage the model to learn cross-chromosomal grammar that
generalizes better. But given 015's strong overdetermination, the
mild loss is the most likely outcome.
"""

import gzip
import math
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
GC_PATH = f"{DATA_DIR}/dhs/dhs_gc.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_SIGNAL = 35_000
N_BREADTH = N_TARGET - N_SIGNAL
N_BINS = 5
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
N_CHROMS = len(VALID_CHROMS)
CAP_RATIO = 1.2
CHROM_CAP = math.ceil(N_TARGET / N_CHROMS * CAP_RATIO)  # 2500


def load_dhs_index():
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    chroms_arr, summits, signals, numsamples = [], [], [], []
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            chroms_arr.append(chrom_to_idx[c])
            summits.append(int(p[6]))
            signals.append(float(p[4]))
            numsamples.append(int(p[5]))
    return (
        np.asarray(chroms_arr, dtype=np.int8),
        np.asarray(summits, dtype=np.int32),
        np.asarray(signals, dtype=np.float32),
        np.asarray(numsamples, dtype=np.float32),
    )


def draw_with_weight(rng, n_to_get, candidate_idx, weights, drawn_global,
                     chrom_idx, summits, chrom_names, chrom_lens, tb,
                     chrom_count, chrom_cap):
    """Draw n_to_get sequences, weighted, respecting a per-chrom cap.

    Skips elements whose chromosome is already at chrom_cap. May
    return fewer than n_to_get if the candidate pool is exhausted
    while too many chromosomes are capped — caller handles short fills.
    """
    sub_w = weights[candidate_idx]
    probs = sub_w / sub_w.sum()
    n_pool = len(candidate_idx)
    seqs: list[str] = []
    batch = max(n_to_get + 5_000, int(n_to_get * 1.2))
    cap_skips = 0
    consecutive_empty = 0
    while len(seqs) < n_to_get:
        n_request = min(batch, n_pool)
        local_idx = rng.choice(n_pool, size=n_request, replace=False, p=probs)
        added_this_pass = 0
        global_idx = [int(candidate_idx[i]) for i in local_idx
                      if int(candidate_idx[i]) not in drawn_global]
        if not global_idx:
            consecutive_empty += 1
            if consecutive_empty >= 3:
                break
            continue
        consecutive_empty = 0
        for i in global_idx:
            drawn_global.add(i)
            c = chrom_names[chrom_idx[i]]
            if chrom_count[c] >= chrom_cap:
                cap_skips += 1
                continue
            s = int(summits[i])
            start, end = s - HALF, s + HALF
            if start < 0 or end > chrom_lens[c]:
                continue
            seq = tb[c][start:end].upper()
            if len(seq) != SEQ_LEN or "N" in seq:
                continue
            seqs.append(seq)
            chrom_count[c] += 1
            added_this_pass += 1
            if len(seqs) >= n_to_get:
                break
        batch = 5_000
        if added_this_pass == 0:
            consecutive_empty += 1
            if consecutive_empty >= 3:
                break
    return seqs[:n_to_get], cap_skips


def main():
    t0 = time.time()
    print(f"Per-chrom cap: {CHROM_CAP} (50000 / 24 * {CAP_RATIO})", flush=True)
    print("Loading DHS Index ...", flush=True)
    chrom_idx, summits, signals, numsamples = load_dhs_index()
    print(f"  {len(chrom_idx):,} rows.", flush=True)

    print("Loading GC content ...", flush=True)
    gc = np.load(GC_PATH)
    valid_mask = ~np.isnan(gc)
    print(f"  {valid_mask.sum():,} valid.", flush=True)

    gc_valid = gc[valid_mask]
    bin_edges = np.percentile(gc_valid, np.linspace(0, 100, N_BINS + 1))
    bin_edges[0] -= 1e-6
    bin_edges[-1] += 1e-6
    print(f"  GC bin edges: {[f'{e:.3f}' for e in bin_edges]}", flush=True)

    bin_idx_per_dhs = np.full(len(gc), -1, dtype=np.int8)
    for b in range(N_BINS):
        in_bin = valid_mask & (gc > bin_edges[b]) & (gc <= bin_edges[b + 1])
        bin_idx_per_dhs[in_bin] = b

    bin_candidates = [np.where(bin_idx_per_dhs == b)[0] for b in range(N_BINS)]
    for b in range(N_BINS):
        print(f"  bin {b}: {len(bin_candidates[b]):,} DHS", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    n_per_bin_signal = N_SIGNAL // N_BINS
    n_per_bin_breadth = N_BREADTH // N_BINS

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        chrom_count: dict[str, int] = {c: 0 for c in chrom_names}
        seqs: list[str] = []
        total_cap_skips = 0
        short_fills = 0

        plan = []
        for b in range(N_BINS):
            plan.append(("signal", b, n_per_bin_signal))
            plan.append(("breadth", b, n_per_bin_breadth))
        rng.shuffle(plan)

        for which, b, n in plan:
            w = signals if which == "signal" else numsamples
            part, cs = draw_with_weight(
                rng, n, bin_candidates[b], w, drawn,
                chrom_idx, summits, chrom_names, chrom_lens, tb,
                chrom_count, CHROM_CAP,
            )
            total_cap_skips += cs
            if len(part) < n:
                short_fills += (n - len(part))
            seqs.extend(part)

        # If short, fill remainder ignoring cap from any GC bin.
        if len(seqs) < N_TARGET:
            need = N_TARGET - len(seqs)
            print(f"  seed={seed}: short {need}, filling without cap", flush=True)
            all_idx = np.where(valid_mask)[0]
            extras, _ = draw_with_weight(
                rng, need, all_idx, signals, drawn,
                chrom_idx, summits, chrom_names, chrom_lens, tb,
                chrom_count, 10**9,  # effectively no cap
            )
            seqs.extend(extras)

        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")

        capped_chroms = sorted(
            [(c, n) for c, n in chrom_count.items() if n >= CHROM_CAP],
            key=lambda x: -x[1],
        )
        print(f"seed={seed}: wrote {len(seqs):,} in "
              f"{time.time() - ts:.1f}s, "
              f"cap_skips={total_cap_skips:,}, "
              f"short_fills={short_fills}, "
              f"capped_chroms={len(capped_chroms)}", flush=True)
        # Show top 5 chrom counts.
        top = sorted(chrom_count.items(), key=lambda x: -x[1])[:5]
        bot = sorted(chrom_count.items(), key=lambda x: x[1])[:5]
        print(f"  top: {top}", flush=True)
        print(f"  bot: {bot}", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
