#!/usr/bin/env python3
"""
Generate 50,000 200 bp sequences for an MPRA library.

Composition (see notebook.md):
  28,000  ENCODE cCREs stratified by class
          (PLS 6k, pELS 6k, dELS 10k, CTCF-only 3k, DNase-H3K4me3 3k)
  13,000  random genomic windows (chr1-22,X,Y)
   4,000  dinucleotide-shuffled cCREs
   2,500  GC-biased random sequences (5 GC% levels)
   2,500  motif-planted synthetic sequences (JASPAR motifs in shuffled bg)

Writes to library/sequences.txt as 50,000 lines of 200 chars in {A,C,G,T}.
"""

import os
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from pyfaidx import Fasta

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "library" / "sequences.txt"

SEQ_LEN = 200
N_TOTAL = 50_000
SEED = 1729
random.seed(SEED)
np.random.seed(SEED)

VALID = set("ACGT")
MAIN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]


# -------------------------------------------------------------- helpers
def upper_clean(seq: str) -> str:
    """Return uppercase {A,C,G,T} string, or None if contains N or other."""
    s = seq.upper()
    if any(c not in VALID for c in s):
        return None
    return s


def valid_200(seq: str) -> bool:
    return len(seq) == SEQ_LEN and set(seq) <= VALID


# -------------------------------------------------------------- genome
print("Loading hg38...", file=sys.stderr)
fa = Fasta(str(DATA / "hg38.fa"), as_raw=True, sequence_always_upper=True)
chrom_lens = {c: len(fa[c]) for c in MAIN_CHROMS}
print(f"  loaded {len(chrom_lens)} chromosomes", file=sys.stderr)


def fetch(chrom: str, start: int, end: int) -> str:
    if start < 0 or end > chrom_lens[chrom]:
        return None
    s = str(fa[chrom][start:end])
    return upper_clean(s)


# -------------------------------------------------------------- cCREs
print("Loading cCREs...", file=sys.stderr)
# class buckets — collapse the CTCF-bound subdivisions back to parent class.
CLASS_MAP = {
    "dELS": "dELS",
    "dELS,CTCF-bound": "dELS",
    "pELS": "pELS",
    "pELS,CTCF-bound": "pELS",
    "PLS": "PLS",
    "PLS,CTCF-bound": "PLS",
    "CTCF-only,CTCF-bound": "CTCF",
    "DNase-H3K4me3": "DNase-H3K4me3",
    "DNase-H3K4me3,CTCF-bound": "DNase-H3K4me3",
}

ccres_by_class = defaultdict(list)
with open(DATA / "GRCh38-cCREs.bed") as f:
    for line in f:
        ch, s, e, _, _, label = line.rstrip("\n").split("\t")
        if ch not in chrom_lens:
            continue
        cls = CLASS_MAP.get(label)
        if cls is None:
            continue
        ccres_by_class[cls].append((ch, int(s), int(e)))
for cls, lst in ccres_by_class.items():
    print(f"  cCRE class {cls}: {len(lst):,}", file=sys.stderr)


def center_200bp(ch: str, s: int, e: int) -> str:
    """Take 200 bp centered on the cCRE midpoint."""
    mid = (s + e) // 2
    a = mid - SEQ_LEN // 2
    b = a + SEQ_LEN
    if a < 0 or b > chrom_lens[ch]:
        return None
    return fetch(ch, a, b)


def sample_ccres(cls: str, n: int) -> list:
    pool = ccres_by_class[cls]
    out = []
    seen = set()
    # shuffle for sampling without replacement
    idx = np.random.permutation(len(pool))
    for i in idx:
        if len(out) >= n:
            break
        rec = pool[i]
        key = (rec[0], (rec[1] + rec[2]) // 2)
        if key in seen:
            continue
        s = center_200bp(*rec)
        if s is None or not valid_200(s):
            continue
        out.append(s)
        seen.add(key)
    return out


# -------------------------------------------------------------- random genomic
def sample_random_genomic(n: int) -> list:
    """Uniform random 200bp windows, weighted by chromosome length."""
    chrom_keys = MAIN_CHROMS
    weights = np.array([chrom_lens[c] for c in chrom_keys], dtype=float)
    weights /= weights.sum()
    out = []
    attempts = 0
    while len(out) < n and attempts < n * 50:
        attempts += 1
        ch = np.random.choice(chrom_keys, p=weights)
        start = np.random.randint(0, chrom_lens[ch] - SEQ_LEN)
        s = fetch(ch, start, start + SEQ_LEN)
        if s is not None and valid_200(s):
            out.append(s)
    return out


# -------------------------------------------------------------- dinuc shuffle
def dinuc_shuffle(seq: str, rng, max_tries: int = 20) -> str:
    """Altschul-Erickson dinucleotide shuffle.

    Builds a random Eulerian path on the de Bruijn graph of dinucleotides;
    result preserves single-nucleotide and dinucleotide composition exactly.
    """
    if len(seq) < 3:
        return seq
    first = seq[0]
    last = seq[-1]

    # Adjacency multiset: from nucleotide -> list of next nucleotides
    base_edges = defaultdict(list)
    for i in range(len(seq) - 1):
        base_edges[seq[i]].append(seq[i + 1])

    nodes = list(base_edges.keys())
    if last not in base_edges:
        # last char has no outgoing edge — fine for an Eulerian PATH endpoint
        pass

    for _try in range(max_tries):
        # Reserve one random outgoing edge per non-terminal node to be used as
        # the LAST edge in the Eulerian path through that node. The chosen
        # "last edges" must form a tree rooted at `last`.
        edges = {n: list(es) for n, es in base_edges.items()}
        last_edges = {}
        ok = True
        for n in nodes:
            if n == last:
                continue
            if not edges[n]:
                continue
            idx = rng.randint(0, len(edges[n]) - 1)
            last_edges[n] = edges[n].pop(idx)

        # Check that following last_edges from each node eventually reaches `last`
        for n in nodes:
            if n == last:
                continue
            cur = n
            seen = {cur}
            steps = 0
            while cur != last:
                if cur not in last_edges:
                    ok = False
                    break
                cur = last_edges[cur]
                if cur in seen:
                    ok = False
                    break
                seen.add(cur)
                steps += 1
                if steps > 8:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue

        # Shuffle remaining edges, then append the reserved last edge at the end
        for n in nodes:
            if n == last:
                rng.shuffle(edges[n])
            else:
                rng.shuffle(edges[n])
                if n in last_edges:
                    edges[n].append(last_edges[n])

        # Walk
        out = [first]
        cur = first
        success = True
        for _ in range(len(seq) - 1):
            if not edges.get(cur):
                success = False
                break
            nxt = edges[cur].pop(0)
            out.append(nxt)
            cur = nxt
        if success and len(out) == len(seq):
            return "".join(out)

    # Fallback: mono shuffle
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)


def sample_shuffled_ccres(n: int) -> list:
    """Take random cCREs, fetch 200bp, dinuc-shuffle."""
    rng = random.Random(SEED + 1)
    # flat pool of all cCREs
    pool = []
    for lst in ccres_by_class.values():
        pool.extend(lst)
    rng.shuffle(pool)
    out = []
    seen = set()
    for rec in pool:
        if len(out) >= n:
            break
        key = (rec[0], (rec[1] + rec[2]) // 2, "shuf")
        if key in seen:
            continue
        s = center_200bp(*rec)
        if s is None or not valid_200(s):
            continue
        shuf = dinuc_shuffle(s, rng)
        if not valid_200(shuf):
            continue
        out.append(shuf)
        seen.add(key)
    return out


# -------------------------------------------------------------- GC-biased random
def sample_gc_biased(n_per_level: int, gc_levels=(0.30, 0.40, 0.50, 0.60, 0.70)) -> list:
    out = []
    for gc in gc_levels:
        p_gc = gc / 2  # split equally between G and C
        p_at = (1 - gc) / 2
        probs = [p_at, p_gc, p_gc, p_at]  # A,C,G,T
        for _ in range(n_per_level):
            arr = np.random.choice(["A", "C", "G", "T"], size=SEQ_LEN, p=probs)
            out.append("".join(arr))
    return out


# -------------------------------------------------------------- motif planting
def parse_jaspar(path: Path) -> list:
    """Parse JASPAR PFM file. Returns list of (name, pfm) where pfm is 4xL float array."""
    motifs = []
    with open(path) as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(">"):
            name = line[1:].split()[0]
            rows = []
            for k in range(4):
                row_line = lines[i + 1 + k]
                # format:  A  [  num num num ... ]
                nums = re.findall(r"\d+\.?\d*", row_line)
                # first number might be in "[ X" pattern; just take all numerics
                rows.append([float(x) for x in nums])
            # length is the min row length (should be consistent)
            L = min(len(r) for r in rows)
            pfm = np.array([r[:L] for r in rows], dtype=float)  # 4 x L
            motifs.append((name, pfm))
            i += 5
        else:
            i += 1
    return motifs


def motif_consensus(pfm: np.ndarray) -> str:
    """Return IUPAC-free consensus: argmax of PFM per column."""
    chars = np.array(["A", "C", "G", "T"])
    return "".join(chars[np.argmax(pfm, axis=0)])


def motif_sample(pfm: np.ndarray, rng) -> str:
    """Sample sequence from PFM probabilistically."""
    probs = pfm / pfm.sum(axis=0, keepdims=True)
    chars = ["A", "C", "G", "T"]
    out = []
    for j in range(pfm.shape[1]):
        out.append(rng.choices(chars, weights=probs[:, j], k=1)[0])
    return "".join(out)


def sample_motif_planted(n: int) -> list:
    rng = random.Random(SEED + 2)
    motifs = parse_jaspar(DATA / "jaspar2024.txt")
    print(f"  loaded {len(motifs)} JASPAR motifs", file=sys.stderr)
    # build shuffled backbone pool from cCREs
    backbone_recs = []
    for lst in ccres_by_class.values():
        backbone_recs.extend(lst)
    rng.shuffle(backbone_recs)

    out = []
    bb_idx = 0
    while len(out) < n and bb_idx < len(backbone_recs):
        rec = backbone_recs[bb_idx]
        bb_idx += 1
        s = center_200bp(*rec)
        if s is None or not valid_200(s):
            continue
        # shuffle the backbone
        bg = dinuc_shuffle(s, rng)
        if not valid_200(bg):
            continue
        # decide number of motifs to plant (1, 2, 3, or 4)
        n_motifs = rng.choices([1, 2, 3, 4], weights=[3, 4, 2, 1], k=1)[0]
        bg_list = list(bg)
        placed = []
        for _ in range(n_motifs):
            name, pfm = rng.choice(motifs)
            ml = pfm.shape[1]
            if ml > SEQ_LEN - 4 or ml < 4:
                continue
            # randomly pick consensus or sampled instance
            mseq = motif_consensus(pfm) if rng.random() < 0.5 else motif_sample(pfm, rng)
            mseq = "".join(c if c in VALID else rng.choice(list(VALID)) for c in mseq)
            # find non-overlapping position
            for _try in range(20):
                pos = rng.randint(0, SEQ_LEN - ml)
                if all(abs(pos - p[0]) >= p[1] for p in placed):
                    placed.append((pos, ml))
                    for j, c in enumerate(mseq):
                        bg_list[pos + j] = c
                    break
            # random strand: with 50% prob, also plant reverse complement
        new = "".join(bg_list)
        if valid_200(new):
            out.append(new)
    return out


# -------------------------------------------------------------- generate
def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    all_seqs = []

    print("Stratum 1: cCREs (PLS) — target 6,000", file=sys.stderr)
    all_seqs.extend(sample_ccres("PLS", 6_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 2: cCREs (pELS) — target 6,000", file=sys.stderr)
    all_seqs.extend(sample_ccres("pELS", 6_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 3: cCREs (dELS) — target 10,000", file=sys.stderr)
    all_seqs.extend(sample_ccres("dELS", 10_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 4: cCREs (CTCF-only) — target 3,000", file=sys.stderr)
    all_seqs.extend(sample_ccres("CTCF", 3_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 5: cCREs (DNase-H3K4me3) — target 3,000", file=sys.stderr)
    all_seqs.extend(sample_ccres("DNase-H3K4me3", 3_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 6: random genomic — target 13,000", file=sys.stderr)
    all_seqs.extend(sample_random_genomic(13_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 7: dinucleotide-shuffled cCREs — target 4,000", file=sys.stderr)
    all_seqs.extend(sample_shuffled_ccres(4_000))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 8: GC-biased random — target 2,500", file=sys.stderr)
    all_seqs.extend(sample_gc_biased(500))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    print("Stratum 9: motif-planted synthetic — target 2,500", file=sys.stderr)
    all_seqs.extend(sample_motif_planted(2_500))
    print(f"  cumulative: {len(all_seqs)}", file=sys.stderr)

    # final validation + (if needed) top-up with random genomic to exactly 50K
    cleaned = []
    for s in all_seqs:
        if valid_200(s):
            cleaned.append(s)
    print(f"  after validation: {len(cleaned)}", file=sys.stderr)

    if len(cleaned) < N_TOTAL:
        topup = N_TOTAL - len(cleaned)
        print(f"  topping up with {topup} random genomic", file=sys.stderr)
        cleaned.extend(sample_random_genomic(topup))
        cleaned = [s for s in cleaned if valid_200(s)]

    cleaned = cleaned[:N_TOTAL]
    assert len(cleaned) == N_TOTAL, f"got {len(cleaned)} sequences, expected {N_TOTAL}"
    for s in cleaned:
        assert valid_200(s), f"invalid sequence (len={len(s)}, chars={set(s)})"

    # shuffle so strata are mixed in the output
    np.random.shuffle(cleaned)

    with open(OUT, "w") as f:
        for s in cleaned:
            f.write(s + "\n")
    print(f"Wrote {len(cleaned)} sequences to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
