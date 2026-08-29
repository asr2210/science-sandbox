"""Experiment 006 — hybrid library combining three signal sources.

Composition (50,000 total):
  - 17,000 TSS-centered RefSeq promoter windows (HepG2-favoring)
  - 16,500 motif-scaffold sequences, hematopoietic-biased pool
    (K562-favoring): GATA1, TAL1, RUNX, ETS, GFI1B, MYB
  - 16,500 motif-scaffold sequences, neural-biased pool
    (SK-N-SH-favoring): NEUROG, NEUROD, BRN2, ASCL1, FOXG1, MEF2,
    plus universal AP-1 / ETS / CREB

Goal: each subset boosts a different cell type so the mean across
cell types should rise. Previous experiments showed each library type
serves only ONE cell type at a time, leaving mean ~0. The hypothesis
is that mixing them lifts all three.

Why this generalizes to unmeasured cell types: the union of
hematopoietic, neural, liver/promoter, and ubiquitous (AP-1, ETS,
CREB) motifs covers a broad TF vocabulary. An unmeasured cell type
will share TFs with at least one subset — the model has seen enough
motif variety to recognize them in a new context, even if it cannot
predict the *magnitude* without retraining.
"""
import os
import re
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
GTF = "data/refGene.gtf"
N = 50_000
N_PROM = 17_000
N_HEMA = 16_500
N_NEUR = N - N_PROM - N_HEMA  # 16,500
L = 200
SEED = 6
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

HEMA_MOTIFS = {
    "GATA1": "AGATAAG",
    "GATA2": "AGATAA",
    "TAL1":  "CAGCTG",         # E-box
    "RUNX":  "TGTGGTT",
    "ETS":   "ACCGGAAGT",
    "GFI1":  "AAATCAC",
    "MYB":   "TAACGGT",
    "KLF1":  "CACACCC",
    "NFE2":  "TGCTGAGTCAT",
    "STAT5": "TTCCCGGAA",
    # universal supporting
    "AP1":   "TGACTCA",
    "USF":   "CACGTG",
    "SP1":   "GGGGTGGGG",
    "CREB":  "TGACGTCA",
}

NEUR_MOTIFS = {
    "NEUROG":  "CAGCTG",       # bHLH E-box
    "NEUROD":  "CAGCTG",
    "ASCL1":   "CAGCTG",
    "BRN2":    "ATGCTAATGC",   # POU
    "FOXG1":   "TGTTTAC",
    "PAX6":    "TTCACGC",
    "REST":    "TCCTGGACAGCGCC",  # neuronal repressor
    "MEF2":    "CTATAAATAG",
    "LHX":     "TAATTA",
    # universal supporting
    "AP1":     "TGACTCA",
    "ETS":     "ACCGGAAGT",
    "USF":     "CACGTG",
    "CREB":    "TGACGTCA",
}

COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A"}


def revcomp(s):
    return s.translate(COMP)[::-1]


def random_backbone(rng, n, L):
    alpha = np.array(list("ACGT"))
    idx = rng.integers(0, 4, size=(n, L))
    return ["".join(alpha[r].tolist()) for r in idx]


def insert_motifs(rng, backbone, motif_pool, n_inserts_lo=4, n_inserts_hi=12):
    keys = list(motif_pool.keys())
    out = []
    for bb in backbone:
        b = list(bb)
        k = int(rng.integers(n_inserts_lo, n_inserts_hi + 1))
        for _ in range(k):
            mk = keys[rng.integers(0, len(keys))]
            m = motif_pool[mk]
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


COMP_BYTES_TABLE = bytes((
    COMP.get(i, chr(i)).encode("ascii")[0] if i in COMP else i
) for i in range(256))


def revcomp_bytes(b):
    return b.translate(COMP_BYTES_TABLE)[::-1]


def sample_promoters(rng, n, L, arrs):
    tss = load_tss()
    idx = rng.permutation(len(tss))
    out = []
    n_rej = 0
    i = 0
    while len(out) < n:
        if i >= len(idx):
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
        out.append(window.decode("ascii"))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    prom = sample_promoters(rng, N_PROM, L, arrs)
    print(f"promoters: {len(prom)} ({time.time()-t0:.1f}s)")

    hema_bb = random_backbone(rng, N_HEMA, L)
    hema = insert_motifs(rng, hema_bb, HEMA_MOTIFS, 4, 12)
    print(f"hematopoietic motif scaff: {len(hema)} ({time.time()-t0:.1f}s)")

    neur_bb = random_backbone(rng, N_NEUR, L)
    neur = insert_motifs(rng, neur_bb, NEUR_MOTIFS, 4, 12)
    print(f"neural motif scaff: {len(neur)} ({time.time()-t0:.1f}s)")

    seqs = prom + hema + neur
    # shuffle so batch order isn't class-correlated
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
