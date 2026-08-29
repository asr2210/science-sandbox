"""Experiment 017 — 35k dense motifs (EXPANDED pool of ~70 TFs) + 15k pELS.

Same recipe as 012 (the best to date) but with the motif vocabulary
roughly doubled. The original 35-motif pool was biased toward known
K562/HepG2/SK-N-SH-relevant TFs. Adding more TFs from other tissues
(more pioneer factors, more housekeeping, more inflammatory, more
developmental) gives the model exposure to a wider grammar.

Generalization angle: a model trained on a broader motif vocabulary
should generalize to unseen cell types whose master regulators may
not overlap with K562/HepG2/SK-N-SH. The 70-motif vocabulary
covers most major TF families (basic helix-loop-helix, zinc finger,
homeobox, bZIP, ETS, MADS, etc.) at roughly equal coverage.

Sources: consensus sequences from JASPAR 2024 CORE collection,
HOCOMOCO v11, and canonical TF binding biology.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_MOTIF = 35_000
N_PELS = N - N_MOTIF
L = 200
SEED = 17
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

# Expanded ~70-motif pool. Original 35 retained; additions cover
# wider TF family diversity.
MOTIFS = {
    # ORIGINAL POOL (kept identical to 012)
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
    # NEW: additional hematopoietic
    "RUNX2":"ACCGCAGTTT","FLI1":"ACAGGAAGT","IKZF1":"TGGGAATGG",
    "E2A":"CAGCTGGT","BCL11A":"GGCCGGAG","SPI1":"GAGGAAGT",
    # NEW: additional liver/metabolic
    "PPARG":"AACTAGGTCA","RXR":"AGGTCAAAGGTCA","SREBP":"ATCACCCCAT",
    "USF2":"CACGTGAC","XBP1":"GATGACGT","ATF4":"TGACGTCA",
    # NEW: additional neural
    "OLIG2":"CAGCTGCC","NEUROG2":"CAGCTGTT","SOX2":"CATTGTT",
    "NRF2":"TGCTGAGTCAT","REST":"TTCAGCACCACGGACAGC",
    "MEF2C":"CTATAAATAGC","NR2F1":"AGGTCAAAGGTCA",
    # NEW: pioneer factors and chromatin openers
    "FOXA2":"TGTTTAC","GATA3":"AGATAAG","NKX2_5":"TCAAGTG",
    "PDX1":"TAATCAGTG","HAND1":"GGCAGCTG","TWIST1":"CAGGTGCAG",
    # NEW: housekeeping / ubiquitous
    "ELK1":"CCGGAAG","GABPA":"CGGAAG","E2F1":"TTTCCCGCC",
    "MYC":"CACGTGGT","MAX":"CACGTG","NFKB":"GGGACTTTCC",
    "TFAP2":"GCCNNNGGC","ZNF143":"GTGCATGCGCA","KLF4":"AGGGGTGGGG",
    # NEW: stress / signaling
    "HIF1A":"ACGTGCGT","STAT3":"TTCCAGGAA","SMAD":"AGCAGCCAGACA",
    "TEAD":"GGAATG","FOXO":"TTGTTTAC","HSF1":"GAANNTTC",
    # NEW: developmental
    "HOXA":"TAATTAA","TBX5":"TCACACCT","PAX3":"GTCACGC",
    "OCT4":"ATGCAAAT","NANOG":"TAATGG","LEF1":"CTTTGTT",
    # NEW: more bZIP and bHLH variants
    "NFAT":"GGAAA","BATF":"TGAGTCAT","JUN":"TGACTCA",
    "FOS":"TGACTCA","BACH1":"TGCTGACTCAGCA","MAFK":"TGCTGAGTCAT",
}
KEYS = list(MOTIFS.keys())
print(f"motif pool size: {len(KEYS)}")
COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A",
        ord("N"): "N"}


def revcomp(s):
    return s.translate(COMP)[::-1]


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
            # If motif has N, replace with random base
            if "N" in m:
                m = "".join(
                    c if c != "N"
                    else "ACGT"[rng.integers(0, 4)] for c in m
                )
            if rng.random() < 0.5:
                m = revcomp(m)
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            b[pos:pos + len(m)] = list(m)
        out.append("".join(b))
    return out


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


def sample_pels(rng, n, L, arrs):
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


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    mot = dense_motifs(rng, N_MOTIF, L)
    pels = sample_pels(rng, N_PELS, L, arrs)
    print(f"motif={len(mot)}, pels={len(pels)} in {time.time()-t0:.1f}s")
    seqs = mot + pels
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
