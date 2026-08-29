"""
Generate a 50,000-sequence MPRA training library (200 bp, ACGT).

Strategy: weighted sampling without replacement from the Meuleman 2020
DHS index (~3.59M elements across 16 NMF components), weighted by
sqrt(mean_signal) to approximate the `dhs_topic` baseline (which sampled
proportional to NMF topic loadings, upweighting strong cell-type-specific
elements). 200bp windows are centred on each DHS summit and extracted from
hg38. Any window containing N is replaced by drawing another element from
the same pool. See notebook.md for the design rationale.
"""

import gzip
import os
import sys
import numpy as np
import pandas as pd
from pyfaidx import Fasta

ROOT = os.path.dirname(os.path.abspath(__file__))
DHS_PATH = os.path.join(ROOT, "data", "dhs_index.txt.gz")
FA_PATH = os.path.join(ROOT, "data", "hg38.fa")
OUT_PATH = os.path.join(ROOT, "library", "sequences.txt")

SEQ_LEN = 200
HALF = SEQ_LEN // 2
TARGET_N = 50000
SEED = 17

VALID_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])


def gumbel_topk_indices(weights: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """Weighted sampling without replacement via the Gumbel-top-k trick.

    Equivalent to numpy.random.choice(p=weights/sum, replace=False) but
    O(n) instead of O(n^2). Returns indices into `weights`.
    """
    # key_i = -log(u_i) / w_i ; pick k smallest keys = weighted sample w/o replacement.
    u = rng.random(len(weights))
    # Guard against log(0): u in [eps, 1)
    eps = np.finfo(np.float64).tiny
    u = np.clip(u, eps, 1.0)
    keys = -np.log(u) / weights
    return np.argpartition(keys, k)[:k]


def extract_window(fa: Fasta, chrom: str, summit: int, chrom_len: int) -> str | None:
    start = summit - HALF
    end = summit + HALF  # pyfaidx is 1-based-ish; using [start:end] gives end-start bp.
    if start < 0 or end > chrom_len:
        return None
    seq = str(fa[chrom][start:end]).upper()
    if len(seq) != SEQ_LEN:
        return None
    if "N" in seq:
        return None
    # Final safety: only ACGT
    if not all(c in "ACGT" for c in seq):
        return None
    return seq


def main():
    rng = np.random.default_rng(SEED)

    print("Loading DHS index ...", file=sys.stderr)
    # Only keep the columns we need; avoids dtype issues on core_start NAs.
    df = pd.read_csv(
        DHS_PATH, sep="\t",
        usecols=["seqname", "mean_signal", "numsamples", "summit", "component"],
        dtype={"seqname": str, "mean_signal": np.float64,
               "numsamples": np.int32, "summit": np.int64, "component": str},
    )
    print(f"  {len(df):,} DHS rows", file=sys.stderr)

    # Restrict to standard chromosomes (already all match, but be safe).
    df = df[df["seqname"].isin(VALID_CHROMS)].reset_index(drop=True)

    chroms = df["seqname"].to_numpy()
    summits = df["summit"].to_numpy()
    signals = df["mean_signal"].to_numpy()

    # sqrt softens the long tail of mean_signal (range ~0.01 to >400).
    weights = np.sqrt(np.maximum(signals, 1e-6))

    print("Opening hg38 ...", file=sys.stderr)
    fa = Fasta(FA_PATH, sequence_always_upper=True, as_raw=True)
    chrom_lens = {c: len(fa[c]) for c in VALID_CHROMS if c in fa}

    # Pull a generous initial pool: 60k indices, take first 50k that yield
    # clean sequences. With N-rejection rate of a few %, this gives ample
    # headroom while only sequencing what we need.
    print("Initial Gumbel-top-k sample ...", file=sys.stderr)
    POOL = TARGET_N + 10000
    chosen = gumbel_topk_indices(weights, POOL, rng)
    rng.shuffle(chosen)  # randomise order so later resamples are independent

    sequences = []
    used = set(int(i) for i in chosen)
    chosen_iter = iter(chosen)

    n_rejected = 0
    refill_round = 0
    while len(sequences) < TARGET_N:
        try:
            idx = int(next(chosen_iter))
        except StopIteration:
            # Need more candidates: re-sample, excluding ones already used.
            refill_round += 1
            print(f"  refilling pool (round {refill_round}) ...", file=sys.stderr)
            mask = np.ones(len(weights), dtype=bool)
            for u in used:
                mask[u] = False
            sub_w = weights.copy()
            sub_w[~mask] = 0.0
            # Sample another 10k candidates from remaining pool.
            need = TARGET_N - len(sequences)
            more = gumbel_topk_indices(sub_w, max(need * 2, 5000), rng)
            chosen_iter = iter(more)
            for u in more:
                used.add(int(u))
            continue
        chrom = chroms[idx]
        clen = chrom_lens.get(chrom)
        if clen is None:
            n_rejected += 1
            continue
        seq = extract_window(fa, chrom, int(summits[idx]), clen)
        if seq is None:
            n_rejected += 1
            continue
        sequences.append(seq)

    print(f"Collected {len(sequences):,} sequences (rejected {n_rejected})", file=sys.stderr)

    # Final shuffle so any structural order in the index doesn't leak in.
    rng.shuffle(sequences)

    assert len(sequences) == TARGET_N
    for s in sequences:
        assert len(s) == SEQ_LEN
        assert set(s) <= set("ACGT")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(sequences) + "\n")
    print(f"Wrote {OUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
