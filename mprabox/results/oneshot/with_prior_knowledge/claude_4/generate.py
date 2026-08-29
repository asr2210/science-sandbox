"""
Generate a 50,000-sequence MPRA training library (200bp each).

Composition:
  37,500 (75%) — DHS elements (Meuleman index), weighted ~proportional to
                 mean_signal across the natural NMF-component distribution.
                 Approximates the proven 'dhs_topic' strategy.
   7,500 (15%) — ENCODE SCREEN cCRE elements, stratified equally across
                 chromatin-state classes (PLS, pELS, dELS, CTCF, etc.).
                 Approximates SEI-style chromatin-state diversity.
   5,000 (10%) — i.i.d. uniform synthetic sequences. Provides noise-floor
                 coverage; empirically helps eval_08-style evals.

All sequences are 200bp, {A,C,G,T} only, extracted from hg38.
Outputs library/sequences.txt (50,000 lines, exactly 200 chars each).
"""

import gzip
import io
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pyfaidx import Fasta

# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
LIB = HERE / "library"
LIB.mkdir(exist_ok=True)

SEQ_LEN = 200
HALF = SEQ_LEN // 2

N_TOTAL = 50_000
N_DHS = 37_500
N_CCRE = 7_500
N_RAND = 5_000
assert N_DHS + N_CCRE + N_RAND == N_TOTAL

SEED = 42
rng = np.random.default_rng(SEED)

VALID_CHARS = set("ACGT")
ALPHABET = np.array(["A", "C", "G", "T"])

# Standard autosomes + X + Y; skip random/unplaced contigs.
CANONICAL_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def extract_window(fa, chrom, center, length=SEQ_LEN):
    """Return uppercase 200bp window centered at `center`, or None if invalid."""
    if chrom not in fa:
        return None
    chrom_len = len(fa[chrom])
    start = center - length // 2
    end = start + length
    if start < 0 or end > chrom_len:
        return None
    seq = str(fa[chrom][start:end]).upper()
    if len(seq) != length:
        return None
    if not set(seq).issubset(VALID_CHARS):
        return None
    return seq


def sample_dhs(fa, n_target):
    """Sample n_target sequences from DHS index, weighted ~ sqrt(mean_signal).

    This emulates the 'dhs_topic' strategy: upweights elements with strong
    NMF topic loadings (mean_signal is correlated with topic strength) while
    preserving the natural distribution across components.
    """
    print(f"[DHS] loading index...", flush=True)
    df = pd.read_csv(
        DATA / "DHS_Index.txt.gz",
        sep="\t",
        low_memory=False,
        usecols=["seqname", "mean_signal", "summit", "component"],
        dtype={
            "seqname": str,
            "mean_signal": np.float32,
            "summit": np.int64,
            "component": str,
        },
    )
    # Keep only canonical chromosomes (skip random/decoy contigs).
    df = df[df["seqname"].isin(CANONICAL_CHROMS)].reset_index(drop=True)
    print(f"[DHS] {len(df):,} elements after chrom filter", flush=True)

    # Sampling weights ~ sqrt(mean_signal). Softer than linear, avoids
    # over-concentrating on the right-tail outliers. Higher signal ≈ stronger
    # NMF topic loading.
    weights = np.sqrt(df["mean_signal"].to_numpy(dtype=np.float64))
    weights = weights / weights.sum()

    seqs = []
    used = set()
    # Oversample because some windows will be discarded (N's, out-of-bounds).
    pool_size = int(n_target * 1.5)
    print(f"[DHS] sampling {pool_size:,} indices...", flush=True)
    candidate_idx = rng.choice(len(df), size=pool_size, replace=False, p=weights)

    summits = df["summit"].to_numpy()
    chroms = df["seqname"].to_numpy()

    for idx in candidate_idx:
        if len(seqs) >= n_target:
            break
        chrom = chroms[idx]
        summit = int(summits[idx])
        seq = extract_window(fa, chrom, summit)
        if seq is None:
            continue
        if seq in used:
            continue
        used.add(seq)
        seqs.append(seq)

    if len(seqs) < n_target:
        # Backup pass: scan more candidates.
        print(f"[DHS] backup pass — have {len(seqs):,} / {n_target:,}", flush=True)
        extra_idx = rng.choice(len(df), size=n_target * 2, replace=False, p=weights)
        for idx in extra_idx:
            if len(seqs) >= n_target:
                break
            chrom = chroms[idx]
            summit = int(summits[idx])
            seq = extract_window(fa, chrom, summit)
            if seq is None or seq in used:
                continue
            used.add(seq)
            seqs.append(seq)

    assert len(seqs) == n_target, f"DHS got {len(seqs)} != {n_target}"
    print(f"[DHS] done: {len(seqs):,} sequences", flush=True)
    return seqs


def sample_ccre(fa, n_target):
    """Sample cCRE sequences, stratified equally across 9 cCRE classes.

    cCREs are 100-500bp regions classified by ENCODE SCREEN. Stratifying
    equally maximizes chromatin-state diversity (~SEI-class behavior).
    """
    print(f"[cCRE] loading...", flush=True)
    cols = ["chrom", "start", "end", "accession", "id", "ccre_class"]
    df = pd.read_csv(
        DATA / "GRCh38-cCREs.bed",
        sep="\t",
        header=None,
        names=cols,
        low_memory=False,
    )
    df = df[df["chrom"].isin(CANONICAL_CHROMS)].reset_index(drop=True)
    df["midpoint"] = ((df["start"] + df["end"]) // 2).astype(np.int64)
    print(f"[cCRE] {len(df):,} elements after chrom filter", flush=True)

    classes = sorted(df["ccre_class"].unique())
    n_classes = len(classes)
    per_class = n_target // n_classes
    leftover = n_target - per_class * n_classes
    # Distribute leftover to the first few (largest) classes.
    class_sizes = df["ccre_class"].value_counts()
    largest = class_sizes.index.tolist()
    target_per_class = {c: per_class for c in classes}
    for i in range(leftover):
        target_per_class[largest[i]] += 1
    print(f"[cCRE] {n_classes} classes, ~{per_class}/class", flush=True)

    seqs = []
    used = set()
    for c, k in target_per_class.items():
        sub = df[df["ccre_class"] == c].reset_index(drop=True)
        # Uniform within class.
        pool_size = min(len(sub), int(k * 1.5))
        idx_pool = rng.choice(len(sub), size=pool_size, replace=False)
        added = 0
        for idx in idx_pool:
            if added >= k:
                break
            seq = extract_window(fa, sub["chrom"].iat[idx], int(sub["midpoint"].iat[idx]))
            if seq is None or seq in used:
                continue
            used.add(seq)
            seqs.append(seq)
            added += 1
        # Backup if class small / many filtered.
        if added < k:
            extra = rng.choice(len(sub), size=min(len(sub), k * 3), replace=False)
            for idx in extra:
                if added >= k:
                    break
                seq = extract_window(fa, sub["chrom"].iat[idx], int(sub["midpoint"].iat[idx]))
                if seq is None or seq in used:
                    continue
                used.add(seq)
                seqs.append(seq)
                added += 1
        print(f"[cCRE]   {c}: {added}/{k}", flush=True)
    assert len(seqs) == n_target, f"cCRE got {len(seqs)} != {n_target}"
    print(f"[cCRE] done: {len(seqs):,} sequences", flush=True)
    return seqs


def sample_random(n_target):
    """Generate i.i.d. uniform random {A,C,G,T} sequences."""
    print(f"[RAND] generating {n_target:,}...", flush=True)
    arr = rng.integers(0, 4, size=(n_target, SEQ_LEN), dtype=np.uint8)
    seqs = [
        "".join(ALPHABET[row].tolist()) for row in arr
    ]
    return seqs


def main():
    print(f"=== Generating MPRA library ({N_TOTAL:,} x {SEQ_LEN}bp) ===", flush=True)
    fa_path = DATA / "hg38.fa"
    if not fa_path.exists():
        sys.exit(f"Missing {fa_path}")
    fa = Fasta(str(fa_path), as_raw=False, sequence_always_upper=False)

    dhs_seqs = sample_dhs(fa, N_DHS)
    ccre_seqs = sample_ccre(fa, N_CCRE)
    rand_seqs = sample_random(N_RAND)

    all_seqs = dhs_seqs + ccre_seqs + rand_seqs
    # Shuffle to avoid any ordering effects in downstream training.
    rng.shuffle(all_seqs)

    # Final validation.
    assert len(all_seqs) == N_TOTAL, len(all_seqs)
    for i, s in enumerate(all_seqs):
        if len(s) != SEQ_LEN or not set(s).issubset(VALID_CHARS):
            sys.exit(f"Invalid sequence at index {i}")

    out = LIB / "sequences.txt"
    with open(out, "w") as fh:
        fh.write("\n".join(all_seqs) + "\n")
    print(f"Wrote {out} ({N_TOTAL:,} sequences)", flush=True)


if __name__ == "__main__":
    main()
