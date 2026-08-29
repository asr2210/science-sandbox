"""Experiment 004: Pure cCRE library with maximum enhancer diversity.

50,000 sequences, all from ENCODE cCREs (no random background), with
distal enhancers (dELS) dominating to maximize regulatory diversity.

Composition:
  - 25,000 dELS (50%; pool=1.47M, most diverse class)
  - 10,000 pELS (20%; pool=243K)
  -  5,000 PLS  (10%; pool=47K, most active but limited pool)
  -  5,000 CA_TF mixed (10%)
  -  5,000 CA-CTCF (10%, separate from other CA — CTCF sites are
            structurally distinctive and underrepresented in 003)

Hypothesis: dropping random background and pushing into the largest
regulatory pool (dELS) will give the model more unique regulatory
grammars to learn. CTCF sites get their own bucket so the model also
sees the structural-element grammar.

Generalization argument: dELS = distal enhancers, which are the most
diverse and cell-type-specific class. Training on a wider variety of
enhancer grammars should help the model generalize to enhancers in
unseen cell types. PLS (promoters) are more conserved and contribute
less marginal information per sequence.

If 004 beats 003: random background was a tax — go further into diverse
regulatory regions. If 004 underperforms 003: random was a useful
"null" example, keep it in future libraries.
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
SEED = 4

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}

TARGETS = {
    "dELS":    25_000,
    "pELS":    10_000,
    "PLS":      5_000,
    "CA_TF":    5_000,
    "CA-CTCF":  5_000,
}


def window_around(start: int, end: int, contig_len: int) -> tuple[int, int]:
    mid = (start + end) // 2
    s = mid - L // 2
    e = s + L
    if s < 0:
        s, e = 0, L
    if e > contig_len:
        e, s = contig_len, contig_len - L
    return s, e


def fetch_clean(fa: Fasta, chrom: str, s: int, e: int) -> str | None:
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
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
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    print("parsing cCREs...")
    by_class: dict[str, list] = {k: [] for k in TARGETS}
    for chrom, s, e, t in parse_bed(BED):
        if t == "PLS":
            grp = "PLS"
        elif t == "pELS":
            grp = "pELS"
        elif t == "dELS":
            grp = "dELS"
        elif t == "CA-CTCF":
            grp = "CA-CTCF"
        else:
            grp = "CA_TF"
        by_class[grp].append((chrom, s, e))
    for k, v in by_class.items():
        print(f"  {k}: {len(v):,} elements")

    seqs: list[str] = []
    for grp, target in TARGETS.items():
        pool = by_class[grp]
        rng.shuffle(pool)
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
        print(f"  {grp}: added {added}/{target}")

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
