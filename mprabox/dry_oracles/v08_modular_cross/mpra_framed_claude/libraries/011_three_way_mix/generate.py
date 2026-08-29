"""Experiment 011 — 3-way mix.

30,000 dense motif scaffolds (60%) +
10,000 TSS-centered RefSeq promoters (20%) +
10,000 PLS-class cCREs (20%) — most-active class of annotated
regulatory elements, centered on midpoint.

Rationale: 009's 70/30 motif+promoter was the best so far. The
heterogeneous eval set rewards diversity. Adding a third type
(PLS cCREs) gives the model exposure to real, high-activity
regulatory sequence with different statistical properties than
either dense motifs or RefSeq TSSs.

Generalization angle: PLS cCREs are real promoters from many cell
types (not K562/HepG2/SK-N-SH-specific). Sequence content reflects
true cross-cell-type promoter grammar, which transfers to unmeasured
cell types where the model needs to recognize promoter-like sequence
in new combinations.
"""
import os
import re
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
GTF = "data/refGene.gtf"
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_MOTIF = 30_000
N_PROM = 10_000
N_CCRE = N - N_MOTIF - N_PROM
L = 200
SEED = 11
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

MOTIFS = {
    "AP1":"TGACTCA","ETS":"ACCGGAAGT","NRF1":"CGCATGCGCA","USF":"CACGTG",
    "SP1":"GGGGTGGGG","CREB":"TGACGTCA",
    "CTCF":"CCCTCTAGTGGCCAGCAGAGGG","NFY":"CCAATCAG","MEF2":"CTATAAATAG",
    "YY1":"CCATCTT","TATA":"TATAAAA","INR":"TCAGTT",
    "GATA1":"AGATAAG","TAL1":"CAGCTG","RUNX":"TGTGGTT","MYB":"TAACGGT",
    "KLF1":"CACACCC","NFE2":"TGCTGAGTCAT","STAT5":"TTCCCGGAA","GFI1B":"AAATCAC",
    "HNF1":"GTTAATAATTAAC","HNF4":"AGGTCAAAGGTCA","FOXA":"TGTTTGTTT",
    "CEBP":"ATTGCGCAAT","PPARA":"AGGTCAAAGGTCA","HNF6":"ATTGATTAA",
    "NEUROD":"GCCAGCTGTT","ASCL1":"AACAGCTGGT","BRN2":"ATGCATAATGC",
    "FOXG1":"TGTTTAC","PAX6":"TTCACGC","LHX":"TAATTAA","TBR1":"TCTAGGTGT",
    "PHOX2":"TAATTG","NRSF":"TCCTGGACAGCGCC",
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
    out = []; i = 0
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


def load_pls_ccres():
    """Load PLS-class cCREs (promoter-like signature, with or without
    CTCF). These are the most active class."""
    out = []
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in CHROMS:
                continue
            cat = p[5]
            # PLS only (with or without CTCF binding)
            if cat == "PLS" or cat == "PLS,CTCF-bound":
                out.append((chrom, int(p[1]), int(p[2])))
    return out


def sample_pls(rng, n, L, arrs):
    pls = load_pls_ccres()
    idx = rng.permutation(len(pls))
    out = []; i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = rng.permutation(len(pls)); i = 0
        chrom, s, e = pls[idx[i]]; i += 1
        mid = (s + e) // 2
        start = mid - L // 2; end = start + L
        if start < 0 or end > len(arrs[chrom]):
            continue
        w = bytes(arrs[chrom][start:end])
        if b"N" in w:
            continue
        out.append(w.decode("ascii"))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    mot = dense_motifs(rng, N_MOTIF, L)
    prom = sample_promoters(rng, N_PROM, L, arrs)
    pls = sample_pls(rng, N_CCRE, L, arrs)
    print(f"motif={len(mot)}, prom={len(prom)}, pls={len(pls)} "
          f"in {time.time()-t0:.1f}s")
    seqs = mot + prom + pls
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
