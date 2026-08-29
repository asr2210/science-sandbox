"""Experiment 008: Cell-type-specific DNase-seq peaks.

50,000 sequences sampled from ENCODE DNase-seq narrowPeak files for
K562, HepG2, and SK-N-SH (200bp peak-centered windows).

Composition:
  - 16,667 K562 DNase peaks (centered ±100bp)
  - 16,666 HepG2 DNase peaks
  - 16,667 SK-N-SH DNase peaks

Hypothesis: cell-type-specific accessibility peaks directly capture
regulatory regions ACTIVE in each measured cell type. This gives the
model labels where activity is known to be high (open chromatin → TF
binding likely → MPRA activity higher than closed chromatin).

Tradeoff: biases the training toward K562/HepG2/SK-N-SH-specific
regulatory grammar (might hurt cross-cell-type generalization). But
the eval sets we are scored on include K562/HepG2/SK-N-SH per-cell
correlations, so any boost to per-cell prediction directly improves
the metric.

Generalization argument: even cell-type-specific peaks contain
universal TF motifs (GATA1 in K562 binds the same motif GATA binds
elsewhere). The model can learn the motif features regardless of
which cell type the peak comes from. The cell-type-specificity
introduces a label-driver signal: same motif at same location, but
the activity differs in the 3 cells, teaching the model how cell
context modulates activity.

If 008 > 003: cell-type-targeted accessibility helps. Combine with
cCREs in future experiments for both breadth and depth.
If 008 < 003: too narrow / cCREs more diverse. Stay with cCREs.
"""
import gzip
import random
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
FA = ROOT / "data" / "hg38.fa"
PEAK_FILES = {
    "K562":   ROOT / "data" / "ENCFF821KDJ.bed.gz",
    "HepG2":  ROOT / "data" / "ENCFF341XEM.bed.gz",
    "SKNSH":  ROOT / "data" / "ENCFF752OZB.bed.gz",
}
OUT = Path(__file__).parent / "sequences_0.txt"
N = 50_000
L = 200
SEED = 8

AUTOSOMES = {f"chr{i}" for i in range(1, 23)}
TARGETS = {"K562": 16_667, "HepG2": 16_666, "SKNSH": 16_667}


def fetch_clean(fa, chrom, s, e):
    seq = str(fa[chrom][s:e]).upper()
    if len(seq) != L or "N" in seq or not set(seq) <= set("ACGT"):
        return None
    return seq


def parse_peaks(path):
    """narrowPeak: yield (chrom, summit_pos)."""
    with gzip.open(path, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in AUTOSOMES:
                continue
            start = int(parts[1])
            end = int(parts[2])
            # narrowPeak: col 10 (peak summit relative to start), 1-based usually
            # If -1, use center
            summit_off = -1
            if len(parts) >= 10:
                try:
                    summit_off = int(parts[9])
                except ValueError:
                    summit_off = -1
            if summit_off >= 0:
                summit = start + summit_off
            else:
                summit = (start + end) // 2
            yield chrom, summit


def main():
    rng = random.Random(SEED)
    print("loading FASTA...")
    fa = Fasta(str(FA), as_raw=True)
    contig_lens = {c: len(fa[c]) for c in AUTOSOMES}

    seqs = []
    seen = set()
    for cell, target in TARGETS.items():
        path = PEAK_FILES[cell]
        peaks = list(parse_peaks(path))
        print(f"  {cell}: {len(peaks):,} peaks loaded from {path.name}")
        rng.shuffle(peaks)
        added = 0
        for chrom, summit in peaks:
            if added >= target:
                break
            ws = summit - L // 2
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
        print(f"  {cell}: added {added}/{target}")

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
