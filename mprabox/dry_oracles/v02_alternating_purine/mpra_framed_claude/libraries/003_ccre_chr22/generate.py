"""
Experiment 003 — 200bp windows centered on chr22 ENCODE cCREs.

Sources:
- chr22 fasta: data/chr22.fa (UCSC hg38)
- cCRE bed: data/GRCh38-cCREs.bed (ENCODE SCREEN registry V3,
  1,063,878 entries genome-wide; 21,578 on chr22)

For each cCRE on chr22 we take a 200bp window centered on the cCRE
midpoint, jittered by a small random offset (±25bp) so identical
cCRE midpoints give different windows on re-sampling. We then sample
50,000 windows with replacement.

This is the natural test of "regulatory enrichment matters".
Compared to experiment 002 (random chr22 windows), the *only* design
difference is window selection: random vs centered on real regulatory
elements. If K562/HepG2 r jumps off zero here, regulatory enrichment
is the missing ingredient.

Choice of chr22-only (vs genome-wide cCREs): clean A/B with experiment
002, isolates the regulatory-enrichment variable. Experiment 004 will
test genome-wide diversity once hg38 finishes downloading.
"""
import os
import numpy as np

N_SEQ = 50_000
L = 200
HALF = L // 2
JITTER = 25     # random shift of window center, ±JITTER bp
SEED = 0
CHR = "chr22"

def load_chr22(fa_path):
    with open(fa_path) as f:
        lines = f.read().splitlines()
    assert lines[0].startswith(">")
    return "".join(lines[1:]).upper()

def load_ccre_chr(bed_path, chrom):
    midpoints = []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] != chrom:
                continue
            start = int(parts[1])
            end = int(parts[2])
            mid = (start + end) // 2
            midpoints.append(mid)
    return np.array(midpoints, dtype=np.int64)

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    fa_path = os.path.join(repo_root, "data", "chr22.fa")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")

    seq = load_chr22(fa_path)
    print(f"chr22 length: {len(seq):,}")
    mids = load_ccre_chr(bed_path, CHR)
    print(f"chr22 cCREs: {len(mids):,}")

    # precompute N prefix sum for fast window-purity check
    arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
    is_n = (arr == ord("N")).astype(np.int32)
    prefix_n = np.concatenate(([0], np.cumsum(is_n)))
    max_start = len(seq) - L

    rng = np.random.default_rng(SEED)
    out = []
    bases = set("ACGT")

    while len(out) < N_SEQ:
        need = N_SEQ - len(out)
        # sample cCREs with replacement
        idx = rng.integers(0, len(mids), size=need * 2)
        jitter = rng.integers(-JITTER, JITTER + 1, size=need * 2)
        centers = mids[idx] + jitter
        starts = centers - HALF
        # clip to valid range
        starts = np.clip(starts, 0, max_start)
        # reject windows containing N
        n_in_window = prefix_n[starts + L] - prefix_n[starts]
        good_starts = starts[n_in_window == 0]
        for s in good_starts:
            if len(out) >= N_SEQ:
                break
            window = seq[int(s):int(s) + L]
            if set(window) <= bases:
                out.append(window)
        if len(good_starts) == 0:
            raise RuntimeError("no good cCRE windows in this batch")

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in out:
            f.write(s)
            f.write("\n")
    with open(out_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == N_SEQ
    assert all(len(s) == L for s in lines)
    assert all(set(s) <= bases for s in lines[:1000])
    gc = sum(1 for line in lines[:5000] for c in line if c in "GC") / (5000 * L)
    print(f"wrote {len(lines)} sequences of length {L} to {out_path}")
    print(f"approximate GC fraction (first 5000): {gc:.3f}")

if __name__ == "__main__":
    main()
