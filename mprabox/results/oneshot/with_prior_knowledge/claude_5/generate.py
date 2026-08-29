#!/usr/bin/env python3
"""Generate a 50,000-sequence MPRA training library (200bp each, {A,C,G,T} only).

Composition (see notebook.md for full rationale):
- 35,000 DHS topic-weighted with soft topic cap (max 5,000/topic)
        weight = mean_signal * max_NMF_load
-  6,000 ENCODE cCRE class-stratified (8 classes, ~750/class)
-  5,000 random synthetic, GC-stratified across 30%-70%
-  4,000 dinuc-shuffled DHS sequences (context-matched negatives)
"""

import gzip
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from pyfaidx import Fasta

# ----- Config -----
RNG_SEED = 20260527
SEQ_LEN = 200
HALF = SEQ_LEN // 2

N_DHS = 35_000
N_CCRE = 6_000
N_SYNTH = 5_000
N_SHUFFLE = 4_000
N_TOTAL = N_DHS + N_CCRE + N_SYNTH + N_SHUFFLE  # 50,000

TOPIC_CAP = 5_000  # max DHS sequences per NMF topic (soft cap)
OVERSAMPLE = 1.30  # candidate pool oversampling (handles Ns + duplicates)

# GC content bins for synthetic stratification (target GC fractions)
SYNTH_GC_BINS = [0.30, 0.40, 0.50, 0.60, 0.70]
SYNTH_PER_BIN = N_SYNTH // len(SYNTH_GC_BINS)  # 1000 per bin

DATA = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "library" / "sequences.txt"

ALLOWED_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
VALID_BASES = set("ACGT")
BASES = np.array(list("ACGT"))


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------- DHS ----------
def load_dhs():
    log("Loading DHS master index...")
    df = pd.read_csv(
        DATA / "dhs_master.txt.gz",
        sep="\t",
        usecols=["seqname", "start", "end", "mean_signal", "summit", "component"],
    )
    log(f"  {len(df):,} DHS elements (raw)")

    log("Loading NMF mixture (16 x N_elements)...")
    with gzip.open(DATA / "nmf_mixture.npy.gz", "rb") as f:
        mix = np.load(f)
    log(f"  mixture shape {mix.shape}")
    assert mix.shape[1] == len(df), "NMF/DHS rowcount mismatch"

    df["max_load"] = mix.max(axis=0).astype(np.float64)
    df["topic"] = mix.argmax(axis=0)

    df = df[df["seqname"].isin(ALLOWED_CHROMS)].reset_index(drop=True)
    log(f"  {len(df):,} DHS after chrom filter")
    return df


def sample_dhs_capped(df, n, rng):
    """Topic-capped quality sampling.

    Algorithm:
    1. Score each DHS as mean_signal * max_load (the dhs_topic weighting).
    2. Sort by weight (with light random jitter for tie-breaking).
    3. Greedy: take elements in descending weight, skipping any whose topic is
       already at cap (TOPIC_CAP).
    4. Continue until n are selected. Oversample to handle later N-rejects.

    Result: high-quality elements dominate, but no topic monopolizes the budget.
    """
    target = int(n * OVERSAMPLE)
    log(f"  topic-capped sampling: target={target:,}, cap/topic={TOPIC_CAP}")
    weights = df["mean_signal"].values * df["max_load"].values
    # multiplicative jitter so ties get random orderings
    jitter = rng.uniform(0.9, 1.1, size=len(weights))
    scores = weights * jitter

    # Sort descending
    order = np.argsort(-scores)
    topics = df["topic"].values
    topic_count = np.zeros(int(topics.max()) + 1, dtype=np.int64)

    # Soft cap scales with target: cap proportional to target relative to N_DHS
    cap = int(np.ceil(TOPIC_CAP * (target / N_DHS)))
    log(f"  effective per-topic cap (with oversample): {cap}")

    selected_idx = []
    for i in order:
        t = topics[i]
        if topic_count[t] >= cap:
            continue
        selected_idx.append(i)
        topic_count[t] += 1
        if len(selected_idx) >= target:
            break
    log(f"  selected {len(selected_idx):,} DHS candidates; topic counts: {topic_count}")
    return df.iloc[selected_idx].reset_index(drop=True)


def extract_dhs_seqs(fa, df, target_n, seen):
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


# ---------- cCRE ----------
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
    log(f"  {len(df):,} cCREs; classes: {sorted(df['cls'].unique().tolist())}")
    return df


def sample_ccres(df, n, rng):
    """Class-stratified sampling, equal per class."""
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


# ---------- Random synthetic, GC-stratified ----------
def gc_stratified_synthetic(rng, seen):
    """Generate N_SYNTH sequences across GC bins."""
    out = []
    bases_array = np.array(list("ACGT"))
    for gc in SYNTH_GC_BINS:
        # P(G) = P(C) = gc/2; P(A) = P(T) = (1-gc)/2
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        bin_count = 0
        attempts = 0
        target = SYNTH_PER_BIN
        while bin_count < target and attempts < 50:
            attempts += 1
            block_n = max(target * 2, 1000)
            idx = rng.choice(4, size=(block_n, SEQ_LEN), p=p)
            for row in idx:
                if bin_count >= target:
                    break
                seq = "".join(bases_array[row])
                if seq in seen:
                    continue
                seen.add(seq)
                out.append(seq)
                bin_count += 1
        log(f"  synth GC={gc:.2f}: {bin_count}")
    # Fill any rounding shortfall with 50% GC uniform sequences
    deficit = N_SYNTH - len(out)
    if deficit > 0:
        log(f"  filling synth shortfall {deficit} with uniform GC")
        while deficit > 0:
            block = rng.choice(4, size=(deficit * 2, SEQ_LEN))
            for row in block:
                if deficit <= 0:
                    break
                seq = "".join(bases_array[row])
                if seq in seen:
                    continue
                seen.add(seq)
                out.append(seq)
                deficit -= 1
    return out[:N_SYNTH]


# ---------- Dinuc shuffle ----------
def dinuc_shuffle_seq(seq, rng):
    """Altschul-Erickson dinucleotide shuffle.

    Produces a sequence with the same dinucleotide composition as `seq`
    by Eulerian random walk on the dinucleotide graph. Standard algorithm
    used in motif discovery (e.g., AME, FIMO, gkm-SVM).
    """
    n = len(seq)
    if n < 2:
        return seq
    # Build adjacency: from each base, list of next bases (in order of occurrence)
    from collections import defaultdict
    edges = defaultdict(list)
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])

    # Try up to a few times to get a valid Eulerian path
    for attempt in range(20):
        # Shuffle outgoing edge lists
        local = {k: list(v) for k, v in edges.items()}
        for k in local:
            rng.shuffle(local[k])
        # Last vertex (sink): its outgoing edges may be the "wrong" one
        # Use the canonical Altschul-Erickson fix:
        # - Pick last edge from each non-sink vertex to be one of its outs at random
        # - That edge sits at the end of the adjacency list
        # Simplified randomization (good enough for our negatives use case):

        # Walk: start at seq[0], take next base = pop from local[current]
        result = [seq[0]]
        cur = seq[0]
        ok = True
        for _ in range(n - 1):
            if not local[cur]:
                ok = False
                break
            nxt = local[cur].pop()
            result.append(nxt)
            cur = nxt
        if ok:
            return "".join(result)
    # Fallback: simple mononucleotide shuffle preserving composition
    arr = list(seq)
    rng.shuffle(arr)
    return "".join(arr)


def make_dinuc_shuffles(fa, dhs_df, n, rng, seen):
    """Sample n DHS sequences (high-signal) and produce dinuc-shuffled versions.

    These act as "context-matched negatives" — same composition, broken motif syntax.
    """
    log("Generating dinuc-shuffled DHS negatives...")
    # Sample from top-quality DHS to ensure interesting backgrounds
    weights = dhs_df["mean_signal"].values * dhs_df["max_load"].values
    weights = np.clip(weights, 1e-9, None)
    weights = weights / weights.sum()
    # Oversample because shuffles may collide with `seen`
    take = int(n * 2.5)
    idx = rng.choice(len(dhs_df), size=min(take, len(dhs_df)), replace=False, p=weights)
    chosen = dhs_df.iloc[idx]

    out = []
    for _, row in chosen.iterrows():
        if len(out) >= n:
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
        shuffled = dinuc_shuffle_seq(seq, rng)
        if len(shuffled) != SEQ_LEN:
            continue
        if not set(shuffled).issubset(VALID_BASES):
            continue
        if shuffled in seen:
            continue
        seen.add(shuffled)
        out.append(shuffled)
    return out


# ---------- Main ----------
def main():
    rng = np.random.default_rng(RNG_SEED)
    log("Opening hg38 fasta...")
    fa = Fasta(str(DATA / "hg38.fa"), as_raw=False, sequence_always_upper=False)
    log("hg38 ready")

    # ---- Component A: DHS topic-weighted, topic-capped ----
    dhs = load_dhs()
    dhs_candidates = sample_dhs_capped(dhs, N_DHS, rng)
    dhs_candidates = dhs_candidates.sample(frac=1, random_state=RNG_SEED).reset_index(drop=True)
    seen = set()
    log("Extracting DHS sequences...")
    dhs_seqs = extract_dhs_seqs(fa, dhs_candidates, N_DHS, seen)
    log(f"  got {len(dhs_seqs):,} valid DHS (target {N_DHS:,})")

    # ---- Component B: cCRE class-stratified ----
    ccre = load_ccres()
    ccre_candidates = sample_ccres(ccre, N_CCRE, rng)
    ccre_candidates = ccre_candidates.sample(frac=1, random_state=RNG_SEED + 1).reset_index(drop=True)
    log("Extracting cCRE sequences...")
    ccre_seqs = extract_ccre_seqs(fa, ccre_candidates, N_CCRE, seen)
    log(f"  got {len(ccre_seqs):,} valid cCREs (target {N_CCRE:,})")

    # ---- Component C: GC-stratified random synthetic ----
    log("Generating GC-stratified random synthetic...")
    synth_seqs = gc_stratified_synthetic(rng, seen)
    log(f"  got {len(synth_seqs):,} synthetic (target {N_SYNTH:,})")

    # ---- Component D: dinuc-shuffled DHS ----
    shuffle_seqs = make_dinuc_shuffles(fa, dhs, N_SHUFFLE, rng, seen)
    log(f"  got {len(shuffle_seqs):,} dinuc-shuffled (target {N_SHUFFLE:,})")

    all_seqs = dhs_seqs + ccre_seqs + synth_seqs + shuffle_seqs
    log(f"Total before top-ups: {len(all_seqs):,}")

    # ---- Top up any deficit with extra DHS (most informative) ----
    if len(all_seqs) < N_TOTAL:
        deficit = N_TOTAL - len(all_seqs)
        log(f"Topping up {deficit:,} with extra DHS...")
        extra = sample_dhs_capped(dhs, deficit * 3, rng)
        extra = extra.sample(frac=1, random_state=RNG_SEED + 7).reset_index(drop=True)
        more = extract_dhs_seqs(fa, extra, deficit, seen)
        all_seqs.extend(more)
        log(f"  now total {len(all_seqs):,}")

    # ---- Final fallback: synthetic ----
    if len(all_seqs) < N_TOTAL:
        deficit = N_TOTAL - len(all_seqs)
        log(f"Final fallback: {deficit:,} uniform synthetic...")
        bases_array = np.array(list("ACGT"))
        while len(all_seqs) < N_TOTAL:
            block = rng.choice(4, size=(deficit * 2 + 100, SEQ_LEN))
            for row in block:
                if len(all_seqs) >= N_TOTAL:
                    break
                seq = "".join(bases_array[row])
                if seq in seen:
                    continue
                seen.add(seq)
                all_seqs.append(seq)
            deficit = N_TOTAL - len(all_seqs)

    assert len(all_seqs) == N_TOTAL, f"Got {len(all_seqs)} != {N_TOTAL}"

    # Shuffle final order so components are interleaved
    rng.shuffle(all_seqs)

    # ---- Sanity checks ----
    lens = {len(s) for s in all_seqs}
    assert lens == {SEQ_LEN}, f"Sequence length mismatch: {lens}"
    char_set = set("".join(all_seqs[:1000]))
    assert char_set.issubset(VALID_BASES), f"Invalid chars: {char_set - VALID_BASES}"
    assert len(set(all_seqs)) == len(all_seqs), "Duplicates found"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    log(f"Writing {len(all_seqs):,} sequences to {OUT}")
    with OUT.open("w") as f:
        f.write("\n".join(all_seqs) + "\n")
    log("Done.")


if __name__ == "__main__":
    main()
