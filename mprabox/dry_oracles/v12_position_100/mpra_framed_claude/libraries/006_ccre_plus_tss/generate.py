"""Experiment 006: cCREs + GENCODE TSS-centered windows.

50,000 sequences = 35K cCREs + 15K GENCODE protein-coding-gene TSS
windows (200bp centered on annotated TSS).

Composition:
- 15K TSS-centered windows from autosomal protein-coding genes
- 20K dELS
-  7K pELS
-  4K PLS
-  4K CA_TF (CA + CA-CTCF + TF + CA-H3K4me3 mixed)

Hypothesis: TSS regions are gold-standard high-activity regulatory
sequences with rich transcription-factor + general-TF motif content
(TATA, INR, GC-box, CpG islands, etc.). Even though cCRE PLS overlaps
many TSS, the TSS annotation is a different categorization and the
±100bp window around each TSS may capture a slightly different
sequence distribution than the PLS-centered window. If different
genomic feature types add complementary information, exp 006 should
beat 003/004.

If 006 ≈ 003: TSS adds nothing beyond cCRE PLS — annotation type
doesn't matter, only sequence content does.
If 006 > 003: TSS captures complementary signal — different genomic
features encode different regulatory grammars.
If 006 < 003: TSS regions are too narrow / oversample the same
sequences — adding TSS hurts diversity.

Generalization argument: TSS-proximal regulatory grammar (promoter
elements, general transcription factor binding sites) is largely
universal across cell types (TBP, GTF2-family TFs are ubiquitous),
so a model that learns TSS context should generalize to any cell type
where active transcription occurs (i.e., all of them).
"""
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
BED = ROOT / "data" / "cCREs.bed"
GTF = ROOT / "data" / "gencode.gtf"
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 6

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

CCRE_TARGETS = {
    "dELS":    20_000,
    "pELS":     7_000,
    "PLS":      4_000,
    "CA_TF":    4_000,
}
N_TSS = 15_000


def window_around(start, end, contig_len):
    mid = (start + end) // 2
    s = mid - L // 2
    e = s + L
    if s < 0: s, e = 0, L
    if e > contig_len: e, s = contig_len, contig_len - L
    return s, e


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_bed(path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def parse_tss(gtf):
    """Yield (chrom, tss_pos) for autosomal protein-coding genes."""
    with open(gtf) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9 or parts[2] != "gene":
                continue
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            if 'gene_type "protein_coding"' not in parts[8]:
                continue
            start = int(parts[3]) - 1  # GTF 1-based, BED 0-based
            end = int(parts[4])
            strand = parts[6]
            tss = start if strand == "+" else end - 1
            yield chrom, tss


def main():
    rng = random.Random(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing TSS from GENCODE...")
    tss_list = list(parse_tss(GTF))
    print(f"  {len(tss_list):,} protein-coding autosomal TSS")

    print("parsing cCREs...")
    by_class = {k: [] for k in CCRE_TARGETS}
    for chrom, s, e, t in parse_bed(BED):
        if t == "PLS": grp = "PLS"
        elif t == "pELS": grp = "pELS"
        elif t == "dELS": grp = "dELS"
        else: grp = "CA_TF"
        by_class[grp].append((chrom, s, e))

    seqs = []
    seen = set()

    # cCREs
    for grp, target in CCRE_TARGETS.items():
        pool = by_class[grp]
        rng.shuffle(pool)
        added = 0
        for chrom, s, e in pool:
            if added >= target:
                break
            ws, we = window_around(s, e, contig_lens[chrom])
            key = (chrom, ws)
            if key in seen:
                continue
            seq = fetch_clean(fa, chrom, ws, we)
            if seq is None:
                continue
            seen.add(key)
            seqs.append(seq)
            added += 1
        print(f"  {grp}: {added}/{target}")

    # TSS
    rng.shuffle(tss_list)
    added = 0
    for chrom, tss in tss_list:
        if added >= N_TSS:
            break
        ws = tss - L // 2
        we = ws + L
        if ws < 0 or we > contig_lens[chrom]:
            continue
        key = (chrom, ws)
        if key in seen:
            continue
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None:
            continue
        seen.add(key)
        seqs.append(seq)
        added += 1
    print(f"  TSS: {added}/{N_TSS}")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} != {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} to {OUT}")


if __name__ == "__main__":
    main()
