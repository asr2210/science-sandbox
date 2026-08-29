#!/usr/bin/env python3
"""Generate a 50,000-sequence MPRA library (200bp each, {A,C,G,T}).

Composition:
- 35,000 DHS elements, weighted by max NMF topic loading * mean_signal
  (proven best single source; cell-type-specific regulatory grammar)
- 10,000 ENCODE cCREs stratified across 8 classes (1,250 each)
  (forces inclusion of promoters, enhancers, CTCF-only, H3K4me3 sites)
-  5,000 random synthetic sequences (i.i.d. uniform {A,C,G,T})
  (sequence-space coverage; helps decoy/uncommon eval sets)

All sequences are extracted as 200bp windows from hg38, centered on the
DHS summit or cCRE midpoint. N-containing sequences are rejected; duplicate
sequences are pruned. The shortfall is backfilled by oversampling each pool.
"""

import gzip
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from pyfaidx import Fasta

# ---------------- Config ----------------
RNG_SEED = 20260527
SEQ_LEN = 200
HALF = SEQ_LEN // 2

# Component counts
N_DHS = 35_000
N_CCRE = 10_000
N_SYNTH = 5_000
N_TOTAL = N_DHS + N_CCRE + N_SYNTH  # 50,000

# Oversampling factors (because some sequences may have Ns or duplicate)
OVERSAMPLE = 1.25

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "library" / "sequences.txt"

# Canonical autosomes + X, Y (exclude alt/random/unplaced/M for stability)
ALLOWED_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

VALID_BASES = set("ACGT")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_dhs():
    log("Loading DHS master index...")
    df = pd.read_csv(
        DATA / "dhs_master.txt.gz",
        sep="\t",
        usecols=["seqname", "start", "end", "mean_signal", "summit", "component"],
    )
    log(f"  {len(df):,} DHS elements")

    log("Loading NMF mixture (16 x N_elements)...")
    with gzip.open(DATA / "nmf_mixture.npy.gz", "rb") as f:
        mix = np.load(f)
    log(f"  mixture shape {mix.shape}")
    assert mix.shape[1] == len(df), "NMF/DHS rowcount mismatch"

    # Max loading across topics (proxy for topic-specificity strength)
    max_load = mix.max(axis=0).astype(np.float64)
    df["max_load"] = max_load
    df["topic_argmax"] = mix.argmax(axis=0)

    # Filter to canonical chroms
    df = df[df["seqname"].isin(ALLOWED_CHROMS)].reset_index(drop=True)
    log(f"  {len(df):,} DHS after chrom filter")
    return df


def sample_dhs(df, n, rng):
    """Sample DHS globally weighted by max_topic_loading * mean_signal.

    Mirrors the dhs_topic strategy (best single baseline): upweights
    elements with strong cell-type-specific accessibility signal. NOT
    equally stratified (dhs_stratified underperformed dhs_topic at 50k).
    """
    w = df["mean_signal"].values * df["max_load"].values
    w = np.clip(w, 1e-9, None)
    w = w / w.sum()
    take = min(int(n * OVERSAMPLE), len(df))
    chosen = rng.choice(len(df), size=take, replace=False, p=w)
    log(f"  DHS sampled (with oversample): {len(chosen):,}")
    return df.iloc[chosen].reset_index(drop=True)


def load_ccres():
    log("Loading ENCODE cCREs...")
    df = pd.read_csv(
        DATA / "ccres.bed",
        sep="\t",
        header=None,
        names=["chrom", "start", "end", "rdhs", "ccre", "cls"],
    )
    df = df[df["chrom"].isin(ALLOWED_CHROMS)].reset_index(drop=True)
    df["mid"] = (df["start"] + df["end"]) // 2
    log(f"  {len(df):,} cCREs after chrom filter; classes: {df['cls'].unique().tolist()}")
    return df


def sample_ccres(df, n, rng):
    """Class-stratified sampling: equal per class to force diversity."""
    classes = sorted(df["cls"].unique())
    per_class = n // len(classes)
    remainder = n - per_class * len(classes)
    indices = []
    for i, cls in enumerate(classes):
        sub = df[df["cls"] == cls]
        take = per_class + (1 if i < remainder else 0)
        take = int(take * OVERSAMPLE)
        take = min(take, len(sub))
        chosen = rng.choice(len(sub), size=take, replace=False)
        indices.append(sub.index.values[chosen])
    all_idx = np.concatenate(indices)
    log(f"  cCRE sampled (with oversample): {len(all_idx):,}")
    return df.loc[all_idx].reset_index(drop=True)


def extract_dhs_seqs(fa, df, target_n, seen):
    """Center 200bp window on summit; reject if N or duplicate; return up to target_n."""
    out = []
    for _, row in df.iterrows():
        if len(out) >= target_n:
            break
        chrom = row["seqname"]
        summit = int(row["summit"])
        s = summit - HALF
        e = summit + HALF
        if s < 0:
            continue
        try:
            seq = str(fa[chrom][s:e]).upper()
        except Exception:
            continue
        if len(seq) != SEQ_LEN:
            continue
        if not set(seq).issubset(VALID_BASES):
            continue
        if seq in seen:
            continue
        seen.add(seq)
        out.append(seq)
    return out


def extract_ccre_seqs(fa, df, target_n, seen):
    out = []
    for _, row in df.iterrows():
        if len(out) >= target_n:
            break
        chrom = row["chrom"]
        mid = int(row["mid"])
        s = mid - HALF
        e = mid + HALF
        if s < 0:
            continue
        try:
            seq = str(fa[chrom][s:e]).upper()
        except Exception:
            continue
        if len(seq) != SEQ_LEN:
            continue
        if not set(seq).issubset(VALID_BASES):
            continue
        if seq in seen:
            continue
        seen.add(seq)
        out.append(seq)
    return out


def random_synthetic(n, rng, seen):
    out = []
    bases = np.array(list("ACGT"))
    # Generate plenty extra, dedup vs seen
    over = int(n * 1.05) + 10
    while len(out) < n:
        block = rng.choice(4, size=(over, SEQ_LEN))
        for row in block:
            if len(out) >= n:
                break
            seq = "".join(bases[row])
            if seq in seen:
                continue
            seen.add(seq)
            out.append(seq)
    return out


def main():
    rng = np.random.default_rng(RNG_SEED)
    fa = Fasta(str(DATA / "hg38.fa"), as_raw=False, sequence_always_upper=False)

    # ---- DHS ----
    dhs = load_dhs()
    dhs_sample = sample_dhs(dhs, N_DHS, rng)
    # Shuffle for randomness in extraction order
    dhs_sample = dhs_sample.sample(frac=1, random_state=RNG_SEED).reset_index(drop=True)
    seen = set()
    log("Extracting DHS sequences...")
    dhs_seqs = extract_dhs_seqs(fa, dhs_sample, N_DHS, seen)
    log(f"  got {len(dhs_seqs):,} valid DHS sequences (target {N_DHS:,})")

    # ---- cCREs ----
    ccre = load_ccres()
    ccre_sample = sample_ccres(ccre, N_CCRE, rng)
    ccre_sample = ccre_sample.sample(frac=1, random_state=RNG_SEED + 1).reset_index(drop=True)
    log("Extracting cCRE sequences...")
    ccre_seqs = extract_ccre_seqs(fa, ccre_sample, N_CCRE, seen)
    log(f"  got {len(ccre_seqs):,} valid cCRE sequences (target {N_CCRE:,})")

    # ---- Random synth ----
    log("Generating random synthetic sequences...")
    synth_seqs = random_synthetic(N_SYNTH, rng, seen)
    log(f"  got {len(synth_seqs):,} synthetic")

    all_seqs = dhs_seqs + ccre_seqs + synth_seqs
    log(f"Total before topping up: {len(all_seqs):,}")

    # If short by any (because of N-rejects), top up from DHS first (most informative)
    if len(all_seqs) < N_TOTAL:
        deficit = N_TOTAL - len(all_seqs)
        log(f"Topping up {deficit:,} from extra DHS samples...")
        # Sample additional DHS elements not already used
        extra = sample_dhs(dhs, deficit * 3, rng)
        extra = extra.sample(frac=1, random_state=RNG_SEED + 2).reset_index(drop=True)
        more = extract_dhs_seqs(fa, extra, deficit, seen)
        all_seqs.extend(more)
        log(f"  now total {len(all_seqs):,}")

    # If still short, top up with random synthetic (always succeeds)
    if len(all_seqs) < N_TOTAL:
        deficit = N_TOTAL - len(all_seqs)
        log(f"Final top-up with {deficit:,} random synthetic...")
        more = random_synthetic(deficit, rng, seen)
        all_seqs.extend(more)

    assert len(all_seqs) == N_TOTAL, f"Got {len(all_seqs)} != {N_TOTAL}"

    # Shuffle final order
    rng.shuffle(all_seqs)

    # Validate
    for i, s in enumerate(all_seqs):
        if len(s) != SEQ_LEN:
            raise ValueError(f"Sequence {i} has length {len(s)} != {SEQ_LEN}")
        if not set(s).issubset(VALID_BASES):
            raise ValueError(f"Sequence {i} has invalid bases")
    if len(set(all_seqs)) != N_TOTAL:
        log(f"WARNING: {N_TOTAL - len(set(all_seqs)):,} duplicates remain")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for s in all_seqs:
            f.write(s + "\n")
    log(f"Wrote {len(all_seqs):,} sequences to {OUT}")


if __name__ == "__main__":
    main()
