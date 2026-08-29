"""Experiment 010 — ENCODE cCRE regulatory regions (PLS+pELS+dELS).

Sample 50k 200bp windows CENTERED on ENCODE Registry V4 cCREs from
chr19 and chr22 that are classified as promoter-like (PLS), proximal
enhancer-like (pELS), or distal enhancer-like (dELS). These are
DNase+TF+H3K4me3/H3K27ac-supported active regulatory regions.

Hypothesis: real regulatory regions score higher than random genomic
tiles, since they are TF-binding-dense and chromatin-accessible.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(10)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

# Load chromosomes
def load_chrom(fa_path):
    parts = []
    with fa_path.open() as f:
        for line in f:
            if line.startswith(">"):
                continue
            parts.append(line.strip().upper())
    return "".join(parts)

chrom_seq = {
    "chr19": load_chrom(DATA / "chr19.fa"),
    "chr22": load_chrom(DATA / "chr22.fa"),
}
print(f"chr19 len: {len(chrom_seq['chr19']):,}; chr22 len: {len(chrom_seq['chr22']):,}")

# Load cCREs for these chroms, keep regulatory classes only
keep = {"PLS", "pELS", "dELS"}
items = []  # (chrom, start, end, cls)
with (DATA / "GRCh38-cCREs.bed").open() as f:
    for line in f:
        ch, s, e, _, _, cls = line.rstrip("\n").split("\t")
        if ch not in chrom_seq:
            continue
        if cls not in keep:
            continue
        items.append((ch, int(s), int(e), cls))
print(f"cCREs (PLS/pELS/dELS) on chr19+chr22: {len(items):,}")

# Sample 200bp window centered on each cCRE; if the cCRE is wider than
# 200bp, pick a random 200bp inside.
out = Path(__file__).parent / "sequences_0.txt"
ok = 0
seen = set()
with out.open("w") as f:
    tries = 0
    while ok < N and tries < N * 5:
        tries += 1
        ch, s, e, _ = items[int(rng.integers(0, len(items)))]
        width = e - s
        if width >= L:
            off = int(rng.integers(0, width - L + 1))
            ps, pe = s + off, s + off + L
        else:
            mid = (s + e) // 2
            ps, pe = mid - L // 2, mid - L // 2 + L
        seq = chrom_seq[ch][ps:pe]
        if len(seq) != L or "N" in seq:
            continue
        key = (ch, ps)
        if key in seen:
            continue
        seen.add(key)
        f.write(seq); f.write("\n")
        ok += 1
print(f"Wrote {ok} sequences to {out}")
