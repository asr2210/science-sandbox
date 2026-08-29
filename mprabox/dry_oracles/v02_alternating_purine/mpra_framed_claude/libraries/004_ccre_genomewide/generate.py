"""
Experiment 004 — genome-wide cCRE-centered 200bp windows.

Sources:
- hg38 fasta: data/hg38.fa
- cCRE bed:   data/GRCh38-cCREs.bed (1,063,878 entries)

Samples 50,000 cCREs without replacement and centers a 200bp window on
each midpoint. Skips windows that overlap N. No jitter needed (we have
21x more cCREs than required, so every sample is a unique element).

Compared to 003 (chr22-only cCRE, ~21K cCREs with ±25bp jitter
resampling), this library:
- has 50,000 unique source elements (no near-duplicates),
- spans the entire genome and all ~1M annotated cCREs,
- represents TF diversity from many cell types, not just chr22's
  parochial subset.

If 004 outperforms 003 substantially → "diversity matters more than
chr22-locality"; cCRE-enrichment is good when paired with full
diversity.

If 004 still loses to 002 (random chr22) → "needs negative examples /
full activity dynamic range"; pure regulatory libraries are still
suboptimal even with maximal diversity. That would refine the theory
sharply.
"""
import os
import time
import numpy as np

N_SEQ = 50_000
L = 200
HALF = L // 2
SEED = 0

def load_hg38(fa_path):
    """Stream hg38.fa, return dict[chrom] -> uppercase sequence string.

    Only main chromosomes (chr1..chr22, chrX, chrY) are kept; alt
    contigs and unplaced scaffolds are skipped.
    """
    main = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
    out = {}
    current = None
    buf = []
    with open(fa_path) as f:
        for line in f:
            if line.startswith(">"):
                if current is not None:
                    out[current] = "".join(buf).upper()
                header = line[1:].strip().split()[0]
                if header in main:
                    current = header
                    buf = []
                else:
                    current = None
                    buf = []
            elif current is not None:
                buf.append(line.rstrip("\n"))
        if current is not None:
            out[current] = "".join(buf).upper()
    return out

def load_ccre(bed_path, keep_chroms):
    """Read bed, return list of (chrom, midpoint)."""
    out = []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in keep_chroms:
                continue
            start = int(parts[1])
            end = int(parts[2])
            mid = (start + end) // 2
            out.append((chrom, mid))
    return out

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    fa_path = os.path.join(repo_root, "data", "hg38.fa")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")

    t0 = time.time()
    print("loading hg38...")
    genome = load_hg38(fa_path)
    print(f"  loaded {len(genome)} chromosomes in {time.time()-t0:.1f}s")
    keep = set(genome.keys())

    t1 = time.time()
    ccres = load_ccre(bed_path, keep)
    print(f"  loaded {len(ccres):,} cCREs in {time.time()-t1:.1f}s")

    # precompute N prefix sums per chromosome
    t2 = time.time()
    n_prefix = {}
    for chrom, seq in genome.items():
        arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
        is_n = (arr == ord("N")).astype(np.int32)
        n_prefix[chrom] = np.concatenate(([0], np.cumsum(is_n)))
    print(f"  N-prefix sums in {time.time()-t2:.1f}s")

    rng = np.random.default_rng(SEED)
    # sample without replacement
    order = rng.permutation(len(ccres))
    bases = set("ACGT")
    out = []
    rejected = 0
    for i in order:
        chrom, mid = ccres[i]
        start = mid - HALF
        seq = genome[chrom]
        if start < 0 or start + L > len(seq):
            rejected += 1
            continue
        if n_prefix[chrom][start + L] - n_prefix[chrom][start] != 0:
            rejected += 1
            continue
        window = seq[start:start + L]
        if not set(window) <= bases:
            rejected += 1
            continue
        out.append(window)
        if len(out) >= N_SEQ:
            break
    print(f"  kept {len(out):,}, rejected {rejected:,} during selection")
    assert len(out) == N_SEQ, f"only got {len(out)}"

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
    print(f"total time: {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
