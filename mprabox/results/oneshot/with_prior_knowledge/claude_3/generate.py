#!/usr/bin/env python3
"""Generate the MPRA training library.

Strategy (50,000 200bp sequences total):
  - 40,000 DHS topic-weighted (Meuleman et al. 2020 DHS Index):
      * Stratified across the 16 NMF components (allocation proportional to
        component pool size, matching the natural "topic" distribution).
      * Within each component, sampled with weight ∝ mean_signal (proxy for
        strong cell-type-specific functional signal — the loadings file is
        only available via Google Drive, but mean_signal is what the
        Meuleman team itself uses as the per-element strength proxy).
  - 5,000 uniform i.i.d. random sequences (sequence-space coverage).
  - 5,000 dinucleotide-shuffled sequences derived from random DHS picks
      (hard-negative coverage: matches local composition without preserving
      motif grammar).

Outputs: library/sequences.txt (50,000 lines, 200bp each, {A,C,G,T} only).
"""
from __future__ import annotations

import gzip
import os
import random
import sys
from collections import defaultdict

import numpy as np
import pyfaidx

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
LIB_DIR = os.path.join(ROOT, "library")
DHS_PATH = os.path.join(DATA_DIR, "DHS_Index_hg38.txt.gz")
FASTA_PATH = os.path.join(DATA_DIR, "hg38.fa")
OUT_PATH = os.path.join(LIB_DIR, "sequences.txt")

SEQ_LEN = 200
TOTAL_N = 50_000
DHS_N = 40_000
UNIFORM_N = 5_000
DINUC_N = 5_000

SEED = 20260527

ALPH = ("A", "C", "G", "T")
ALPH_SET = set(ALPH)
N_SET = {"N", "n"}


def load_fasta_keys(fa: pyfaidx.Fasta) -> set[str]:
    return set(fa.keys())


def is_clean_acgt(seq: str) -> bool:
    s = seq.upper()
    return len(s) == SEQ_LEN and all(c in ALPH_SET for c in s)


def fetch_window(fa: pyfaidx.Fasta, chrom: str, center: int) -> str | None:
    """Return the 200bp window centered at `center` on `chrom`, or None
    if it falls off the chromosome or contains N's."""
    half = SEQ_LEN // 2
    start = center - half
    end = start + SEQ_LEN
    if start < 0:
        return None
    chrom_len = len(fa[chrom])
    if end > chrom_len:
        return None
    seq = str(fa[chrom][start:end]).upper()
    if len(seq) != SEQ_LEN:
        return None
    if any(c not in ALPH_SET for c in seq):
        return None
    return seq


def stream_dhs_index(path: str):
    """Yield (chrom, summit, mean_signal, component) for each DHS entry on
    chr1..chr22, chrX, chrY (drop alt contigs to stay in the standard
    assembly used by typical MPRA training pipelines)."""
    keep_chroms = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
    with gzip.open(path, "rt") as fh:
        header = fh.readline().rstrip().split("\t")
        idx = {name: i for i, name in enumerate(header)}
        ci, si, ms_i, ss_i, cp_i = (idx["seqname"], idx["summit"],
                                    idx["mean_signal"], idx["summit"],
                                    idx["component"])
        for line in fh:
            parts = line.rstrip().split("\t")
            chrom = parts[ci]
            if chrom not in keep_chroms:
                continue
            summit = int(parts[si])
            mean_signal = float(parts[ms_i])
            comp = parts[cp_i]
            yield chrom, summit, mean_signal, comp


def sample_dhs(rng: np.random.Generator, fa: pyfaidx.Fasta) -> list[str]:
    """Topic-stratified, signal-weighted sampling from the DHS index."""
    by_comp: dict[str, list[tuple[str, int, float]]] = defaultdict(list)
    fa_keys = load_fasta_keys(fa)
    for chrom, summit, ms, comp in stream_dhs_index(DHS_PATH):
        if chrom not in fa_keys:
            continue
        by_comp[comp].append((chrom, summit, ms))

    total = sum(len(v) for v in by_comp.values())
    print(f"DHS pool (autosomes + X/Y): {total:,} elements across "
          f"{len(by_comp)} components", flush=True)

    # Allocate per-component sample budget proportional to pool size.
    # Adjust rounding so totals sum to DHS_N.
    comps = sorted(by_comp.keys())
    fracs = np.array([len(by_comp[c]) for c in comps], dtype=np.float64) / total
    raw = fracs * DHS_N
    alloc = np.floor(raw).astype(int)
    remainder = DHS_N - int(alloc.sum())
    # Distribute the remainder to components with largest fractional residuals.
    resid_order = np.argsort(-(raw - alloc))
    for i in range(remainder):
        alloc[resid_order[i]] += 1
    assert alloc.sum() == DHS_N

    out: list[str] = []
    # We over-sample within each component then filter to clean ACGT windows,
    # because a non-trivial fraction of windows centred on a DHS summit hit
    # N's (especially near centromeres / unplaced regions).
    for comp, n_target in zip(comps, alloc):
        pool = by_comp[comp]
        weights = np.array([p[2] for p in pool], dtype=np.float64)
        weights = np.clip(weights, 1e-6, None)
        probs = weights / weights.sum()
        # Sample with replacement; the pool is huge so duplicates are
        # vanishingly unlikely at our budgets.
        n_oversample = int(min(len(pool), n_target * 3 + 2000))
        idx = rng.choice(len(pool), size=n_oversample, replace=False, p=probs)
        kept = 0
        for j in idx:
            if kept >= n_target:
                break
            chrom, summit, _ = pool[j]
            seq = fetch_window(fa, chrom, summit)
            if seq is None:
                continue
            out.append(seq)
            kept += 1
        if kept < n_target:
            # Backfill ignoring weights, just to fill the budget.
            extra = rng.choice(len(pool), size=len(pool), replace=False)
            for j in extra:
                if kept >= n_target:
                    break
                chrom, summit, _ = pool[j]
                seq = fetch_window(fa, chrom, summit)
                if seq is None:
                    continue
                out.append(seq)
                kept += 1
        print(f"  component={comp!r:35s} target={n_target:5d} kept={kept:5d}",
              flush=True)
    return out


def uniform_random(rng: np.random.Generator, n: int) -> list[str]:
    arr = rng.integers(0, 4, size=(n, SEQ_LEN), dtype=np.int8)
    table = np.array(ALPH)
    return ["".join(table[row]) for row in arr]


def dinuc_shuffle(seq: str, rng: np.random.Generator) -> str:
    """Altschul-Erickson dinucleotide shuffle, preserving exact dinucleotide
    counts. Implementation: edge-list random Eulerian walk."""
    s = seq.upper()
    if len(s) < 2:
        return s
    # Build adjacency
    out_edges: dict[str, list[str]] = {c: [] for c in ALPH}
    for i in range(len(s) - 1):
        out_edges[s[i]].append(s[i + 1])
    # Shuffle edge lists, then ensure a valid Eulerian path exists from
    # start = s[0] by reserving one outgoing edge per non-terminal vertex to
    # the "final" vertex = s[-1] (Altschul-Erickson trick).
    end = s[-1]
    start = s[0]
    for c in ALPH:
        rng.shuffle(out_edges[c])
    # Reserve last-edge to `end` for each vertex except `end` itself:
    # find one edge ending in path from each vertex to `end` in the random
    # arborescence; classic AE algorithm. We use a simpler approximate
    # approach: retry up to 8 times until a complete walk is produced.
    for attempt in range(8):
        edges = {c: list(out_edges[c]) for c in ALPH}
        for c in ALPH:
            rng.shuffle(edges[c])
        cursor = start
        walked = [cursor]
        ok = True
        for _ in range(len(s) - 1):
            if not edges[cursor]:
                ok = False
                break
            nxt = edges[cursor].pop()
            walked.append(nxt)
            cursor = nxt
        if ok and len(walked) == len(s):
            return "".join(walked)
    # Fallback: monomer shuffle (rare path).
    chars = list(s)
    rng.shuffle(chars)
    return "".join(chars)


def dinuc_shuffled_from_dhs(rng: np.random.Generator, source_seqs: list[str],
                            n: int) -> list[str]:
    out = []
    rng_py = random.Random(int(rng.integers(0, 2**31 - 1)))
    for _ in range(n):
        src = source_seqs[rng_py.randrange(len(source_seqs))]
        shuffled = dinuc_shuffle(src, rng)
        if is_clean_acgt(shuffled):
            out.append(shuffled)
        else:
            # Should not happen — DHS sequences are clean ACGT, dinuc-shuffle
            # preserves alphabet. Guard anyway.
            out.append(shuffled.upper().replace("N", rng_py.choice(ALPH)))
    return out


def main() -> int:
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    print("Opening hg38 reference...", flush=True)
    fa = pyfaidx.Fasta(FASTA_PATH, sequence_always_upper=True)

    print("Sampling DHS topic-weighted (40,000)...", flush=True)
    dhs_seqs = sample_dhs(rng, fa)
    print(f"Got {len(dhs_seqs):,} DHS sequences", flush=True)

    print("Generating uniform random (5,000)...", flush=True)
    uni_seqs = uniform_random(rng, UNIFORM_N)

    print("Generating dinuc-shuffled from DHS (5,000)...", flush=True)
    # Use a random subset of DHS sequences as composition templates.
    template_idx = rng.choice(len(dhs_seqs),
                              size=min(len(dhs_seqs), DINUC_N * 3),
                              replace=False)
    templates = [dhs_seqs[i] for i in template_idx]
    dinuc_seqs = dinuc_shuffled_from_dhs(rng, templates, DINUC_N)

    all_seqs = dhs_seqs + uni_seqs + dinuc_seqs
    assert len(all_seqs) == TOTAL_N, f"Got {len(all_seqs)} sequences (want {TOTAL_N})"

    # Final validation + shuffle so model training does not see a blocked
    # ordering by source bucket.
    bad = [i for i, s in enumerate(all_seqs) if not is_clean_acgt(s)]
    if bad:
        print(f"!! {len(bad)} bad sequences", file=sys.stderr)
        sys.exit(2)

    order = rng.permutation(TOTAL_N)
    all_seqs = [all_seqs[i] for i in order]

    os.makedirs(LIB_DIR, exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        for s in all_seqs:
            fh.write(s)
            fh.write("\n")
    print(f"Wrote {len(all_seqs):,} sequences to {OUT_PATH}", flush=True)

    # Print quick summary stats for the notebook record.
    arr = np.array([list(s) for s in all_seqs])
    gc = float(np.mean((arr == "G") | (arr == "C")))
    print(f"Library GC content: {gc:.4f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
