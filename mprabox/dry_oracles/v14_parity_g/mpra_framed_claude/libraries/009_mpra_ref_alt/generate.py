"""Experiment 009: ref + alt allele pairs from Tewhey lab MPRA TSVs.

For each variant in the K562/SK-N-SH MPRA TSVs (excl chr7/13),
generate BOTH the ref-allele 200bp sequence AND the alt-allele 200bp
sequence. This gives the model paired contrast: near-identical sequences
with different activities, which is what Malinois was trained on.

Source:
- K562   ENCFF141ZOX.tsv (493k variant×allele rows)
- SK-N-SH ENCFF521IVN.tsv (251k variant×allele rows)

Each TSV row has chr/pos/ref_allele/alt_allele/allele=ref|alt. We
reconstruct sequences by:
- Extract hg38[chr][pos-100 : pos+100] (1-based pos, so adjust to 0-based)
- Confirm reference base at center position matches ref_allele
- For alt: replace center base with alt_allele
- Skip indels (multi-base ref/alt) for simplicity

Sample 25,000 unique variant locations and emit ref+alt = 50,000 lines.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
TSVS = [
    os.path.join(ROOT, "data", "ENCFF141ZOX.tsv"),  # K562
    os.path.join(ROOT, "data", "ENCFF521IVN.tsv"),  # SK-N-SH
]
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"7", "13"}

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

# Collect unique (chr, pos, ref, alt) variants from any TSV
variants = set()
for tsv in TSVS:
    with open(tsv) as f:
        header = f.readline().rstrip().split("\t")
        idx = {col: i for i, col in enumerate(header)}
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[idx["chr"]]
            if chrom in EXCLUDE_CHR or chrom == "X" or chrom == "NA":
                continue
            pos_str = cols[idx["pos"]]
            if pos_str in ("NA", ""):
                continue
            pos = int(pos_str)
            ref = cols[idx["ref_allele"]]
            alt = cols[idx["alt_allele"]]
            if len(ref) != 1 or len(alt) != 1:
                continue
            variants.add((chrom, pos, ref, alt))

print(f"unique variants: {len(variants)}")

variants = list(variants)
rng.shuffle(variants)

pair_seqs = []  # list of (ref_seq, alt_seq)
for chrom, pos, ref, alt in variants:
    chrom_full = f"chr{chrom}"
    if chrom_full not in fa.keys():
        continue
    chrlen = len(fa[chrom_full])
    # 1-based to 0-based: pos-1 is the center base
    start = pos - 1 - L // 2
    end = start + L
    if start < 0 or end > chrlen:
        continue
    seq = str(fa[chrom_full][start:end])
    if "N" in seq or len(seq) != L:
        continue
    center = L // 2  # center index in seq corresponds to pos
    if seq[center] != ref.upper():
        # genome doesn't match expected ref — skip
        continue
    alt_seq = seq[:center] + alt.upper() + seq[center + 1:]
    pair_seqs.append((seq, alt_seq))
    if len(pair_seqs) == 25_000:
        break

print(f"got {len(pair_seqs)} ref+alt pairs ({len(pair_seqs)*2} sequences)")
assert len(pair_seqs) == 25_000

all_seqs = []
for r, a in pair_seqs:
    all_seqs.append(r)
    all_seqs.append(a)

rng.shuffle(all_seqs)
assert len(all_seqs) == 50_000
for s in all_seqs:
    assert len(s) == L
    assert set(s) <= set("ACGT")

with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {len(all_seqs)} to {OUT}")
