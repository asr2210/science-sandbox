"""Experiment 016 — 35k structured-syntax motifs + 15k pELS.

Hypothesis: real enhancers depend on TF cooperativity (homotypic
clusters + specific TF pairs). Random motif placement (007-015)
loses these cooperative features. A model trained on syntax-rich
sequences should learn TF-cooperation features that generalize
better.

Motif scaffold composition (35k total):
- 12k homotypic clusters: 3-5 of SAME motif within ~30 bp window.
- 12k TF-pair syntax: known co-binding pairs at biological spacings:
    * GATA1 + TAL1 (hematopoietic, ~10 bp apart)
    * HNF1 + HNF4 (liver, ~50 bp apart)
    * NEUROD + ASCL1 (neural, ~20 bp apart)
    * AP1 + ETS (general, ~5-15 bp)
    * SP1 + ETS (housekeeping, ~10-30 bp)
- 11k standard mixed (control): same as 007/012 recipe.

Plus the proven 15k pELS slot from 012.

Generalization angle: TF pairs and homotypic clusters are evolution-
conserved features of regulatory grammar. The same TF family pairs
recur in different cell types. A model that learns syntax (not just
motif counts) transfers better to unseen cell types.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_HOMOTYPIC = 12_000
N_PAIRED = 12_000
N_MIXED = 11_000
N_PELS = 15_000
L = 200
SEED = 16
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

# Known cooperative TF pairs (biologically realistic spacings in bp)
PAIRS = [
    ("GATA1", "TAL1", 4, 15),
    ("HNF1", "HNF4", 30, 70),
    ("NEUROD", "ASCL1", 10, 30),
    ("AP1", "ETS", 4, 15),
    ("SP1", "ETS", 8, 25),
    ("FOXA", "HNF4", 10, 30),
    ("CEBP", "AP1", 5, 20),
    ("RUNX", "ETS", 5, 15),
    ("KLF1", "GATA1", 10, 40),
    ("CREB", "AP1", 5, 20),
]


def revcomp(s):
    return s.translate(COMP)[::-1]


def random_backbone(rng, n, L):
    alpha = np.array(list("ACGT"))
    bb_idx = rng.integers(0, 4, size=(n, L))
    return ["".join(alpha[r].tolist()) for r in bb_idx]


def insert_motif(b, m, pos, rng):
    if rng.random() < 0.5:
        m = revcomp(m)
    end = pos + len(m)
    if end > len(b):
        return
    b[pos:end] = list(m)


def homotypic_seqs(rng, n, L):
    backbones = random_backbone(rng, n, L)
    out = []
    for i in range(n):
        b = list(backbones[i])
        # 2-3 homotypic clusters per sequence
        n_clusters = int(rng.integers(2, 4))
        for _ in range(n_clusters):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if len(m) >= 60:
                continue
            # 3-5 copies in ~30-60 bp window
            n_copies = int(rng.integers(3, 6))
            window_w = max(60, n_copies * (len(m) + 4))
            window_start = int(rng.integers(0, max(1, L - window_w)))
            for _ in range(n_copies):
                pos = window_start + int(
                    rng.integers(0, max(1, window_w - len(m)))
                )
                insert_motif(b, m, pos, rng)
        # Also add 5-10 random motifs as backbone noise
        n_random = int(rng.integers(5, 11))
        for _ in range(n_random):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            insert_motif(b, m, pos, rng)
        out.append("".join(b))
    return out


def paired_seqs(rng, n, L):
    backbones = random_backbone(rng, n, L)
    out = []
    for i in range(n):
        b = list(backbones[i])
        # 2-3 cooperative pairs per sequence
        n_pairs = int(rng.integers(2, 4))
        for _ in range(n_pairs):
            pa, pb, sp_min, sp_max = PAIRS[
                rng.integers(0, len(PAIRS))
            ]
            ma, mb = MOTIFS[pa], MOTIFS[pb]
            spacing = int(rng.integers(sp_min, sp_max + 1))
            pair_len = len(ma) + spacing + len(mb)
            if pair_len >= L:
                continue
            pos = int(rng.integers(0, L - pair_len + 1))
            insert_motif(b, ma, pos, rng)
            insert_motif(b, mb, pos + len(ma) + spacing, rng)
        # Plus 5-10 random motifs for background
        n_random = int(rng.integers(5, 11))
        for _ in range(n_random):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            insert_motif(b, m, pos, rng)
        out.append("".join(b))
    return out


def mixed_seqs(rng, n, L):
    """Same as 012 recipe — random mix of 15-25 motifs."""
    backbones = random_backbone(rng, n, L)
    out = []
    n_inserts = rng.integers(15, 26, size=n)
    for i in range(n):
        b = list(backbones[i])
        for _ in range(int(n_inserts[i])):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            insert_motif(b, m, pos, rng)
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
    hom = homotypic_seqs(rng, N_HOMOTYPIC, L)
    pai = paired_seqs(rng, N_PAIRED, L)
    mix = mixed_seqs(rng, N_MIXED, L)
    pels = sample_pels(rng, N_PELS, L, arrs)
    print(f"hom={len(hom)} pair={len(pai)} mix={len(mix)} "
          f"pels={len(pels)} in {time.time()-t0:.1f}s")
    seqs = hom + pai + mix + pels
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
