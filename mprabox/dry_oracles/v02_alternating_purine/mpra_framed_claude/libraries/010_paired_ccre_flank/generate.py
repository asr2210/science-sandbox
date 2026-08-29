"""
Experiment 010 — paired cCRE + 1kb-flanking (informative negatives).

Composition (50K total):
- 25,000 cCRE-centered 200bp windows (positives, sampled w/o replacement
  from ~1M genome-wide cCREs).
- 25,000 flanking windows: for each chosen cCRE, take a 200bp window
  shifted by ±1500 to ±3000 bp from the cCRE midpoint. Direction
  (+/-) and exact offset chosen uniformly per pair. Flanks that fall
  in another annotated cCRE are dropped and re-sampled; this gives
  *true* non-regulatory paired negatives from the same chromosomal
  neighborhood.

Hypothesis: harder negatives (from the same regulatory neighborhood)
force the model to actually find motifs rather than learn the coarse
"intergenic vs gene-rich neighborhood" distinction.

Predicted vs 005 (50/50 random + uniform cCRE, 0.156):
- if model needs hard negatives → 010 beats 005 (better K562/HepG2,
  similar SK-N-SH)
- if model benefits from diverse easy negatives → 010 loses to 005

Generalization rationale: a model trained with informative paired
negatives learns *what specifically* makes a sequence regulatory
(presence/density of motifs), which should transfer better to unseen
cell types than learning "regulatory neighborhood vs intergenic".
"""
import os, time, numpy as np

N_PAIRS = 25_000
L = 200
HALF = L // 2
FLANK_MIN = 1500
FLANK_MAX = 3000
SEED = 0

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    genome, n_prefix = {}, {}
    for f in sorted(os.listdir(cache_dir)):
        if f.endswith(".npy"):
            c = f[:-4]
            mat = np.asarray(np.load(os.path.join(cache_dir, f), mmap_mode="r"))
            genome[c] = mat
            is_n = (mat == ord("N")).astype(np.int32)
            n_prefix[c] = np.concatenate(([0], np.cumsum(is_n)))
    chroms = sorted(genome.keys())
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")
    rng = np.random.default_rng(SEED)

    # Build per-chr interval arrays (start, end) for cCRE-overlap check.
    ccre_intervals = {c: [] for c in chroms}
    cidx = {c: i for i, c in enumerate(chroms)}
    all_mids = []  # (chrom, mid) for sampling
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome:
                continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            mid = (s + e) // 2
            all_mids.append((c, mid))
    # sort intervals per chrom for binary search
    for c in chroms:
        ccre_intervals[c].sort()
    print(f"  {len(all_mids):,} cCREs loaded, {time.time()-t0:.1f}s")

    def overlaps_ccre(chrom, start, end):
        """Binary-search whether [start, end) overlaps any cCRE interval."""
        intervals = ccre_intervals[chrom]
        # find rightmost interval with s < end
        lo, hi = 0, len(intervals)
        while lo < hi:
            m = (lo + hi) // 2
            if intervals[m][0] < end:
                lo = m + 1
            else:
                hi = m
        # check the few candidates near lo
        for k in range(max(0, lo - 2), min(len(intervals), lo + 1)):
            s2, e2 = intervals[k]
            if s2 < end and start < e2:
                return True
        return False

    order = rng.permutation(len(all_mids))
    positives, flanks = [], []

    idx = 0
    while len(positives) < N_PAIRS and idx < len(order):
        c, mid = all_mids[order[idx]]
        idx += 1
        # positive: cCRE-centered
        p_start = mid - HALF
        if p_start < 0 or p_start + L > len(genome[c]):
            continue
        if n_prefix[c][p_start + L] - n_prefix[c][p_start] != 0:
            continue
        # try to find a flank in this neighborhood
        flank_found = None
        for try_i in range(8):  # 8 tries
            sign = 1 if rng.random() < 0.5 else -1
            offset = sign * rng.integers(FLANK_MIN, FLANK_MAX + 1)
            f_start = mid + int(offset) - HALF
            if f_start < 0 or f_start + L > len(genome[c]):
                continue
            if n_prefix[c][f_start + L] - n_prefix[c][f_start] != 0:
                continue
            if overlaps_ccre(c, f_start, f_start + L):
                continue
            flank_window = genome[c][f_start:f_start + L].tobytes().decode("ascii")
            if not set(flank_window) <= bases:
                continue
            flank_found = flank_window
            break
        if flank_found is None:
            continue
        positive_window = genome[c][p_start:p_start + L].tobytes().decode("ascii")
        if not set(positive_window) <= bases:
            continue
        positives.append(positive_window)
        flanks.append(flank_found)

    print(f"  positives: {len(positives)}; flanks: {len(flanks)} (took {idx} cCREs to find {len(positives)} valid pairs)")
    assert len(positives) == N_PAIRS

    all_seqs = positives + flanks
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == 50_000

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote 50000 → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
