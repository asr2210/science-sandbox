"""Experiment 003: Real human genomic regulatory regions (ENCODE cCREs).

50,000 sequences sampled from hg38 at ENCODE Registry V4 cCRE coordinates,
balanced across regulatory classes plus a random-genomic-background
component.

Composition:
  - 12,500 PLS  (promoter-like)
  - 12,500 pELS (proximal enhancer-like)
  - 12,500 dELS (distal enhancer-like, subsampled)
  -  6,250 mixed CA*/TF (chromatin-accessible / TF-bound)
  -  6,250 random autosomal background (non-cCRE intervals)

Each cCRE is centered to a 200bp window. Random background draws random
200bp from autosomes. N-containing windows are rejected.

Hypothesis: real genomic regulatory sequence has natural motif content
AND natural sequence context. The model should learn the universal
cis-regulatory grammar much better than from synthetic motif insertion
in random background.

Generalization argument: regulatory grammar (TF motifs, their spacing,
co-occurrence) is shared across cell types. A model trained on a
diverse panel of human regulatory regions has the chance to learn this
grammar, and the learned grammar should transfer to any cell type
because TF binding is sequence-driven.
"""
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
BED = ROOT / "data" / "cCREs.bed"
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 3

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

TARGETS = {
    "PLS": 12_500,
    "pELS": 12_500,
    "dELS": 12_500,
    "CA_TF": 6_250,
    "RANDOM": 6_250,
}


def window_around(start: int, end: int, contig_len: int) -> tuple[int, int]:
    mid = (start + end) // 2
    s = mid - L // 2
    e = s + L
    if s < 0:
        s = 0
        e = L
    if e > contig_len:
        e = contig_len
        s = e - L
    return s, e


def fetch_clean(fa: Fasta, chrom: str, start: int, end: int) -> str | None:
    seq = str(fa[chrom][start:end]).upper()
    if len(seq) != L:
        return None
    if "N" in seq:
        return None
    if not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_bed(path: Path):
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            yield chrom, int(parts[1]), int(parts[2]), parts[5]


def main():
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)
    print("loading FASTA index...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs.bed...")
    by_class: dict[str, list] = {k: [] for k in ("PLS", "pELS", "dELS", "CA_TF")}
    for chrom, s, e, t in parse_bed(BED):
        if t == "PLS":
            grp = "PLS"
        elif t == "pELS":
            grp = "pELS"
        elif t == "dELS":
            grp = "dELS"
        else:
            grp = "CA_TF"
        by_class[grp].append((chrom, s, e))
    for k, v in by_class.items():
        print(f"  {k}: {len(v):,} elements")

    seqs: list[str] = []

    for grp in ("PLS", "pELS", "dELS", "CA_TF"):
        pool = by_class[grp]
        rng.shuffle(pool)
        target = TARGETS[grp]
        added = 0
        seen = set()
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
        print(f"  {grp}: added {added} (target {target})")

    print("sampling random background...")
    chrom_list = sorted(AUTOSOMES, key=lambda c: int(c[3:]))
    chrom_weights = np.array([contig_lens[c] for c in chrom_list], dtype=float)
    chrom_weights /= chrom_weights.sum()
    target = TARGETS["RANDOM"]
    added = 0
    tries = 0
    while added < target and tries < 1_000_000:
        tries += 1
        chrom = nprng.choice(chrom_list, p=chrom_weights)
        clen = contig_lens[chrom]
        start = int(nprng.integers(0, clen - L))
        seq = fetch_clean(fa, chrom, start, start + L)
        if seq is None:
            continue
        seqs.append(seq)
        added += 1
    print(f"  RANDOM: added {added} (target {target}) after {tries} tries")

    if len(seqs) != N:
        raise RuntimeError(f"got {len(seqs)} sequences, expected {N}")

    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s)
            f.write("\n")
    print(f"wrote {N} sequences to {OUT}")


if __name__ == "__main__":
    main()
