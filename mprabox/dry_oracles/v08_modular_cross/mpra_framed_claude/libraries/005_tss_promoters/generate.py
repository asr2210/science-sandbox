"""Experiment 005 — TSS-centered RefSeq promoter windows.

Sample TSS positions from RefSeq transcripts and extract a 200 bp
window centered on the TSS (-100..+100). Most TSSs are highly active
in MPRA because they evolved to recruit Pol II.

If random genomic and cCREs both gave r~0, but promoters give r > 0,
that confirms (a) the model needs sequences with reliably HIGH activity
to learn from, and (b) promoter-class sequence is intrinsically more
informative than enhancer-class.

Generalization angle: promoter grammar (TATA, INR, CpG islands, GC
content) is universal — protein-coding gene promoters in K562 are
substantially the same as in any other human cell type, with cell-
type-specific TF binding layered on top. So a promoter library should
transfer.
"""
import os
import time
import re
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
GTF = "data/refGene.gtf"
N = 50_000
L = 200
SEED = 5
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])


def load_tss():
    seen = set()
    tss_list = []
    pat = re.compile(r'gene_name "([^"]+)"')
    with open(GTF) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9 or parts[2] != "transcript":
                continue
            chrom, start, end, strand = parts[0], int(parts[3]), int(parts[4]), parts[6]
            if chrom not in CHROMS:
                continue
            m = pat.search(parts[8])
            gene = m.group(1) if m else parts[8]
            tss = start if strand == "+" else end
            key = (chrom, tss, strand, gene)
            if key in seen:
                continue
            seen.add(key)
            tss_list.append((chrom, tss, strand))
    return tss_list


COMP = {ord("A"): ord("T"), ord("C"): ord("G"),
        ord("G"): ord("C"), ord("T"): ord("A"),
        ord("N"): ord("N")}


def revcomp_bytes(b):
    return bytes(x for x in b)[::-1].translate(bytes(COMP[i] if i in COMP else i
                                                     for i in range(256)))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    tss = load_tss()
    print(f"loaded {len(tss)} unique TSSs in {time.time()-t0:.1f}s")
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r") for c in CHROMS}
    idx = rng.permutation(len(tss))
    seqs = []
    n_rej = 0
    i = 0
    while len(seqs) < N:
        if i >= len(idx):
            # cycle by re-permuting
            idx = rng.permutation(len(tss))
            i = 0
        chrom, t, strand = tss[idx[i]]
        i += 1
        start = t - L // 2
        end = start + L
        if start < 0 or end > len(arrs[chrom]):
            n_rej += 1
            continue
        window = bytes(arrs[chrom][start:end])
        if b"N" in window:
            n_rej += 1
            continue
        if strand == "-":
            window = revcomp_bytes(window)
        seqs.append(window.decode("ascii"))
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N} seqs in {time.time()-t0:.1f}s ({n_rej} rejects)")


if __name__ == "__main__":
    main()
