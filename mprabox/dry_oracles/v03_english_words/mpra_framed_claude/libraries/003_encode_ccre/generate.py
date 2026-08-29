"""
003 — ENCODE cCRE library.

Sample 50,000 candidate cis-regulatory elements (cCREs) from the
ENCODE Registry V4 (GRCh38), extract a 200bp window centered on each
cCRE midpoint from hg38, and write to sequences_0.txt.

Sampling weights span enhancer-like, promoter-like, CTCF, TF, and
chromatin-accessible elements so the library covers diverse regulatory
grammars across cell types — not just K562/HepG2/SK-N-SH motif palette.
"""
import numpy as np
from pathlib import Path
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

BED = DATA / "GRCh38-cCREs.V4.bed"
FA = DATA / "hg38.fa"

L = 200
N = 50_000
SEED = 3

# Type → target count.
TARGETS = {
    "dELS":       25_000,  # distal enhancer-like
    "pELS":       10_000,  # proximal enhancer-like
    "PLS":         7_000,  # promoter-like
    "TF":          3_000,  # TF binding only
    "CA-CTCF":     2_000,  # CTCF + accessible
    "CA":          3_000,  # accessible only
}
assert sum(TARGETS.values()) == N

# Standard chromosomes (autosomes + X, Y). Skip chrM and alt contigs.
CHROMS_OK = {f"chr{c}" for c in list(range(1, 23)) + ["X", "Y"]}

rng = np.random.default_rng(SEED)

# Load BED.
print("Loading BED...")
records = {k: [] for k in TARGETS}
with BED.open() as fh:
    for line in fh:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 6:
            continue
        chrom, start, end, _id1, _id2, etype = fields[:6]
        if chrom not in CHROMS_OK:
            continue
        if etype not in records:
            continue
        records[etype].append((chrom, int(start), int(end)))

for k, v in records.items():
    print(f"  {k}: {len(v)} available, target {TARGETS[k]}")

# Sample each pool independently.
selected = []
for etype, n_target in TARGETS.items():
    pool = records[etype]
    if len(pool) < n_target:
        # Should not happen with V4 but just in case.
        chosen_idx = rng.integers(0, len(pool), size=n_target)
    else:
        chosen_idx = rng.choice(len(pool), size=n_target, replace=False)
    for i in chosen_idx:
        chrom, start, end = pool[i]
        mid = (start + end) // 2
        wstart = mid - L // 2
        wend = wstart + L
        selected.append((chrom, wstart, wend, etype))

rng.shuffle(selected)

print(f"Extracting {len(selected)} windows from hg38...")
fa = Fasta(str(FA), as_raw=True, sequence_always_upper=True)

ALPHA = set("ACGT")
out_lines = []
skipped_oob = 0
skipped_n = 0
for chrom, ws, we, etype in selected:
    if ws < 0 or we > len(fa[chrom]):
        skipped_oob += 1
        continue
    seq = str(fa[chrom][ws:we]).upper()
    if len(seq) != L:
        skipped_oob += 1
        continue
    if not set(seq).issubset(ALPHA):
        # Contains N or other ambiguity — replace any non-ACGT with a random base.
        # If too many Ns (>5), skip.
        non_acgt = sum(1 for c in seq if c not in ALPHA)
        if non_acgt > 5:
            skipped_n += 1
            continue
        seq = "".join(c if c in ALPHA else "ACGT"[rng.integers(0, 4)] for c in seq)
    out_lines.append(seq)

print(f"skipped (OOB): {skipped_oob}, (Ns>5): {skipped_n}, kept: {len(out_lines)}")

# Top up if we skipped any.
if len(out_lines) < N:
    print(f"Topping up {N - len(out_lines)} more from dELS pool (most abundant)...")
    pool = records["dELS"]
    while len(out_lines) < N:
        i = int(rng.integers(0, len(pool)))
        chrom, start, end = pool[i]
        mid = (start + end) // 2
        wstart = mid - L // 2
        wend = wstart + L
        if wstart < 0 or wend > len(fa[chrom]):
            continue
        seq = str(fa[chrom][wstart:wend]).upper()
        if len(seq) != L:
            continue
        if not set(seq).issubset(ALPHA):
            non_acgt = sum(1 for c in seq if c not in ALPHA)
            if non_acgt > 5:
                continue
            seq = "".join(c if c in ALPHA else "ACGT"[rng.integers(0, 4)] for c in seq)
        out_lines.append(seq)

# Truncate if somehow over.
out_lines = out_lines[:N]

with OUT.open("w") as f:
    for s in out_lines:
        f.write(s)
        f.write("\n")

print(f"wrote {len(out_lines)} x {L}bp sequences to {OUT}")
