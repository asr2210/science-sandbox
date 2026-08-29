"""Experiment 008 — 50/50 dense motif scaffolds + TSS promoters.

25,000 dense motif scaffolds (15-25 motifs, same broad pool as exp 007)
+ 25,000 TSS-centered promoter windows (strand-corrected). Goal: stack
the two best-performing sub-libraries to push mean_r above the
individual maxes.

Generalization rationale: the union covers two kinds of regulatory
grammar a model needs to know:
- "designed/synthetic motif-rich enhancer" (the dense scaffolds)
- "natural promoter with CpG islands, TATA-like patches, Sp1 sites"
  (the TSS windows)

A model that learns both will recognize either pattern in a new cell
type. Real cell types in the wild use the same TF families, just in
different combinations, so the motif vocabulary transfers even when
the activity magnitudes do not.
"""
import os
import re
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
GTF = "data/refGene.gtf"
N = 50_000
N_MOTIF = 25_000
N_PROM = N - N_MOTIF
L = 200
SEED = 8
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

MOTIFS = {
    "AP1":    "TGACTCA",
    "ETS":    "ACCGGAAGT",
    "NRF1":   "CGCATGCGCA",
    "USF":    "CACGTG",
    "SP1":    "GGGGTGGGG",
    "CREB":   "TGACGTCA",
    "CTCF":   "CCCTCTAGTGGCCAGCAGAGGG",
    "NFY":    "CCAATCAG",
    "MEF2":   "CTATAAATAG",
    "YY1":    "CCATCTT",
    "TATA":   "TATAAAA",
    "INR":    "TCAGTT",
    "GATA1":  "AGATAAG",
    "TAL1":   "CAGCTG",
    "RUNX":   "TGTGGTT",
    "MYB":    "TAACGGT",
    "KLF1":   "CACACCC",
    "NFE2":   "TGCTGAGTCAT",
    "STAT5":  "TTCCCGGAA",
    "GFI1B":  "AAATCAC",
    "HNF1":   "GTTAATAATTAAC",
    "HNF4":   "AGGTCAAAGGTCA",
    "FOXA":   "TGTTTGTTT",
    "CEBP":   "ATTGCGCAAT",
    "PPARA":  "AGGTCAAAGGTCA",
    "HNF6":   "ATTGATTAA",
    "NEUROD": "GCCAGCTGTT",
    "ASCL1":  "AACAGCTGGT",
    "BRN2":   "ATGCATAATGC",
    "FOXG1":  "TGTTTAC",
    "PAX6":   "TTCACGC",
    "LHX":    "TAATTAA",
    "TBR1":   "TCTAGGTGT",
    "PHOX2":  "TAATTG",
    "NRSF":   "TCCTGGACAGCGCC",
}
KEYS = list(MOTIFS.keys())
COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A"}
COMP_TABLE = bytes((
    {ord("A"): ord("T"), ord("C"): ord("G"),
     ord("G"): ord("C"), ord("T"): ord("A"),
     ord("N"): ord("N")}.get(i, i)
) for i in range(256))


def revcomp(s):
    return s.translate(COMP)[::-1]


def revcomp_bytes(b):
    return b.translate(COMP_TABLE)[::-1]


def dense_motifs(rng, n, L):
    alpha = np.array(list("ACGT"))
    bb_idx = rng.integers(0, 4, size=(n, L))
    backbone = ["".join(alpha[r].tolist()) for r in bb_idx]
    n_inserts = rng.integers(15, 26, size=n)
    out = []
    for i in range(n):
        b = list(backbone[i])
        for _ in range(int(n_inserts[i])):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if rng.random() < 0.5:
                m = revcomp(m)
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            b[pos:pos + len(m)] = list(m)
        out.append("".join(b))
    return out


def load_tss():
    seen = set()
    out = []
    pat = re.compile(r'gene_name "([^"]+)"')
    with open(GTF) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 9 or p[2] != "transcript":
                continue
            chrom, s, e, strand = p[0], int(p[3]), int(p[4]), p[6]
            if chrom not in CHROMS:
                continue
            m = pat.search(p[8])
            g = m.group(1) if m else p[8]
            tss = s if strand == "+" else e
            key = (chrom, tss, strand, g)
            if key in seen:
                continue
            seen.add(key)
            out.append((chrom, tss, strand))
    return out


def sample_promoters(rng, n, L, arrs):
    tss = load_tss()
    idx = rng.permutation(len(tss))
    out = []
    i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = rng.permutation(len(tss)); i = 0
        chrom, t, strand = tss[idx[i]]; i += 1
        start = t - L // 2; end = start + L
        if start < 0 or end > len(arrs[chrom]):
            continue
        w = bytes(arrs[chrom][start:end])
        if b"N" in w:
            continue
        if strand == "-":
            w = revcomp_bytes(w)
        out.append(w.decode("ascii"))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    mot = dense_motifs(rng, N_MOTIF, L)
    print(f"motif scaff: {len(mot)} in {time.time()-t0:.1f}s")
    prom = sample_promoters(rng, N_PROM, L, arrs)
    print(f"promoters: {len(prom)} in {time.time()-t0:.1f}s")
    seqs = mot + prom
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
