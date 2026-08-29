"""Experiment 022 — Motif-enhanced real pELS backbone + pure pELS.

35k real pELS sequences with 10-20 motifs inserted into each
+ 15k pure pELS sequences (unchanged).

Hypothesis: real pELS backbone contains genomic statistics (k-mer
distribution, CpG content, flanking patterns) that a model can learn
alongside TF features. Random ACGT backbone may lack these signals.
Motif-enhanced real pELS = best of both worlds: real genomic context
+ explicit TF binding patterns.

Generalization angle: unseen cell types have regulatory elements in
realistic genomic contexts, not random sequences. A model trained on
real genomic backbones should transfer better than one trained on
random + motifs alone.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_ENHANCED = 35_000
N_PURE = N - N_ENHANCED
L = 200
SEED = 22
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


def revcomp(s):
    return s.translate(COMP)[::-1]


def load_pels():
    out = []
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in CHROMS:
                continue
            cat = p[5]
            if cat == "pELS" or cat == "pELS,CTCF-bound":
                out.append((chrom, int(p[1]), int(p[2])))
    return out


def sample_pels_backbones(rng, n, L, arrs):
    pels = load_pels()
    idx = rng.permutation(len(pels))
    out = []; i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = rng.permutation(len(pels)); i = 0
        chrom, s, e = pels[idx[i]]; i += 1
        mid = (s + e) // 2
        start = mid - L // 2; end = start + L
        if start < 0 or end > len(arrs[chrom]):
            continue
        w = bytes(arrs[chrom][start:end])
        if b"N" in w:
            continue
        out.append(w.decode("ascii"))
    return out


def enhance_with_motifs(rng, backbones, n_low, n_high, L):
    n_inserts = rng.integers(n_low, n_high + 1, size=len(backbones))
    out = []
    for i, bb in enumerate(backbones):
        b = list(bb)
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


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    # Sample 50k pELS sequences total
    all_pels = sample_pels_backbones(rng, N, L, arrs)
    # First 35k become motif-enhanced backbones
    enhanced = enhance_with_motifs(rng, all_pels[:N_ENHANCED],
                                   10, 20, L)
    pure = all_pels[N_ENHANCED:]
    print(f"enhanced={len(enhanced)}, pure={len(pure)} "
          f"in {time.time()-t0:.1f}s")
    seqs = enhanced + pure
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
