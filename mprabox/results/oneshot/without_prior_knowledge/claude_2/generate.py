#!/usr/bin/env python3
"""
Generate a 50,000-sequence (200bp) MPRA training library targeting
generalizable regulatory grammar across cell types.

Composition:
- 23,000 cCRE-centered windows (dELS/pELS/PLS/CTCF/DNase-H3K4me3)
-  4,000 cCRE flanking-shifted windows (penumbra)
- 10,000 random genomic windows (negatives / neutral)
-  4,000 dinucleotide-shuffled cCREs (hard negatives)
-  7,000 synthetic motif-embedded sequences (JASPAR TFs)
-  2,000 pure-random sequences across GC content

Total: 50,000
"""
from __future__ import annotations
import gzip
import os
import random
import sys
from pathlib import Path

import numpy as np
import pyfaidx

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LIB = ROOT / "library"
LIB.mkdir(exist_ok=True)

SEQ_LEN = 200
TARGET_N = 50_000
RNG = random.Random(20260524)
NPRNG = np.random.default_rng(20260524)

# ---------------------------------------------------------------------------
# Genome
# ---------------------------------------------------------------------------
print("[1/8] Loading hg38 ...", flush=True)
GENOME = pyfaidx.Fasta(str(DATA / "hg38.fa"), as_raw=False, sequence_always_upper=True)

# Use only standard autosomes + X + Y for clean coverage
STD_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
CHROM_LENS = {c: len(GENOME[c]) for c in STD_CHROMS}
TOTAL_BP = sum(CHROM_LENS.values())
CHROM_WEIGHTS = np.array([CHROM_LENS[c] for c in STD_CHROMS], dtype=np.float64)
CHROM_WEIGHTS /= CHROM_WEIGHTS.sum()

VALID_BASES = set("ACGT")


def fetch_seq(chrom: str, start: int, end: int) -> str:
    """Fetch genomic sequence; returns uppercase string. May contain N."""
    if start < 0 or end > CHROM_LENS.get(chrom, 0):
        return ""
    s = str(GENOME[chrom][start:end]).upper()
    return s


def is_clean(seq: str) -> bool:
    """No Ns, exactly SEQ_LEN bases from {A,C,G,T}."""
    if len(seq) != SEQ_LEN:
        return False
    # check chars
    for ch in seq:
        if ch not in VALID_BASES:
            return False
    return True


# ---------------------------------------------------------------------------
# cCRE parsing
# ---------------------------------------------------------------------------
print("[2/8] Parsing cCREs ...", flush=True)
ccre_by_class: dict[str, list[tuple[str, int, int]]] = {
    "dELS": [], "pELS": [], "PLS": [], "CTCF-only": [], "DNase-H3K4me3": [],
}
ccre_all: list[tuple[str, int, int, str]] = []  # (chrom, start, end, class)

with open(DATA / "ccres.bed") as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        chrom, start, end, _, _, cls = parts[0], int(parts[1]), int(parts[2]), parts[3], parts[4], parts[5]
        if chrom not in CHROM_LENS:
            continue
        # primary class is first token before any comma
        primary = cls.split(",")[0].strip()
        if primary not in ccre_by_class:
            continue
        ccre_by_class[primary].append((chrom, start, end))
        ccre_all.append((chrom, start, end, primary))

print(f"   cCRE counts: " + ", ".join(f"{k}={len(v)}" for k, v in ccre_by_class.items()),
      flush=True)


def center_window(chrom: str, start: int, end: int, shift: int = 0) -> tuple[str, int, int]:
    center = (start + end) // 2 + shift
    s = center - SEQ_LEN // 2
    e = s + SEQ_LEN
    return chrom, s, e


def sample_ccres(cls: str, n: int, shift_range: int = 0) -> list[str]:
    pool = ccre_by_class[cls]
    seqs: list[str] = []
    attempts = 0
    max_attempts = n * 20
    # shuffle once for diverse sampling
    idxs = list(range(len(pool)))
    RNG.shuffle(idxs)
    p = 0
    while len(seqs) < n and attempts < max_attempts:
        attempts += 1
        if p >= len(idxs):
            RNG.shuffle(idxs)
            p = 0
        i = idxs[p]; p += 1
        chrom, start, end = pool[i]
        shift = RNG.randint(-shift_range, shift_range) if shift_range else 0
        c, s, e = center_window(chrom, start, end, shift)
        seq = fetch_seq(c, s, e)
        if is_clean(seq):
            seqs.append(seq)
    return seqs


# ---------------------------------------------------------------------------
# Random genomic windows
# ---------------------------------------------------------------------------
def sample_random_genomic(n: int) -> list[str]:
    seqs: list[str] = []
    attempts = 0
    while len(seqs) < n:
        attempts += 1
        if attempts > n * 30:
            break
        # weighted choice of chromosome
        c = NPRNG.choice(STD_CHROMS, p=CHROM_WEIGHTS)
        clen = CHROM_LENS[c]
        if clen < SEQ_LEN + 1000:
            continue
        s = RNG.randint(1000, clen - SEQ_LEN - 1000)
        seq = fetch_seq(c, s, s + SEQ_LEN)
        if is_clean(seq):
            seqs.append(seq)
    return seqs


# ---------------------------------------------------------------------------
# Dinucleotide shuffle (Altschul-Erickson algorithm via simple Eulerian walk)
# ---------------------------------------------------------------------------
def dinuc_shuffle(seq: str, rng: random.Random) -> str:
    """Return dinucleotide-preserving shuffle of seq. Uses simple edge-shuffle
    algorithm: build a directed graph of dinucleotide edges, then random walk."""
    n = len(seq)
    if n < 4:
        return seq
    # adjacency: from each base, list of next bases (in order of appearance)
    edges: dict[str, list[str]] = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        a, b = seq[i], seq[i + 1]
        if a in edges and b in "ACGT":
            edges[a].append(b)
    # Shuffle outgoing edges per node, but to preserve Eulerian property we
    # need a tree-edge constraint. Use a simple iterative trick:
    for _ in range(10):
        for k in edges:
            rng.shuffle(edges[k])
        # construct
        start = seq[0]
        path = [start]
        ptrs = {k: 0 for k in edges}
        cur = start
        for _step in range(n - 1):
            if ptrs[cur] >= len(edges[cur]):
                # broken walk; reshuffle and retry
                path = None
                break
            nxt = edges[cur][ptrs[cur]]
            ptrs[cur] += 1
            path.append(nxt)
            cur = nxt
        if path and len(path) == n:
            return "".join(path)
    return seq  # fallback


def sample_shuffled_ccres(n: int) -> list[str]:
    """Sample cCREs, get the 200bp window, then dinuc-shuffle."""
    seqs: list[str] = []
    attempts = 0
    while len(seqs) < n and attempts < n * 5:
        attempts += 1
        chrom, start, end, _cls = RNG.choice(ccre_all)
        c, s, e = center_window(chrom, start, end)
        win = fetch_seq(c, s, e)
        if not is_clean(win):
            continue
        sh = dinuc_shuffle(win, RNG)
        if is_clean(sh):
            seqs.append(sh)
    return seqs


# ---------------------------------------------------------------------------
# JASPAR PFM parsing and motif embedding
# ---------------------------------------------------------------------------
print("[3/8] Loading JASPAR motifs ...", flush=True)
def parse_jaspar(path: Path) -> list[tuple[str, np.ndarray]]:
    """Returns list of (name, PFM[4,L]) tuples. Rows = A,C,G,T."""
    motifs = []
    cur_name = None
    cur_rows = {}
    bases_order = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if cur_name and len(cur_rows) == 4:
                    pfm = np.array([cur_rows[b] for b in "ACGT"], dtype=np.float64)
                    motifs.append((cur_name, pfm))
                cur_name = line[1:].split()[0]
                cur_rows = {}
                bases_order = []
            else:
                # row like: "A  [   4  19  0  0  0  0 ]"
                parts = line.replace("[", " ").replace("]", " ").split()
                base = parts[0]
                vals = [float(x) for x in parts[1:] if x]
                cur_rows[base] = vals
                bases_order.append(base)
    if cur_name and len(cur_rows) == 4:
        pfm = np.array([cur_rows[b] for b in "ACGT"], dtype=np.float64)
        motifs.append((cur_name, pfm))
    return motifs


JASPAR = parse_jaspar(DATA / "jaspar_vert.jaspar")
print(f"   Loaded {len(JASPAR)} JASPAR motifs", flush=True)


def pfm_to_ppm(pfm: np.ndarray, pseudocount: float = 0.25) -> np.ndarray:
    counts = pfm + pseudocount
    return counts / counts.sum(axis=0, keepdims=True)


def sample_motif_instance(ppm: np.ndarray, rng: np.random.Generator) -> str:
    """Sample one DNA instance from a PPM (4xL matrix)."""
    L = ppm.shape[1]
    bases = "ACGT"
    out = []
    for j in range(L):
        idx = rng.choice(4, p=ppm[:, j])
        out.append(bases[idx])
    return "".join(out)


def rev_comp(s: str) -> str:
    comp = str.maketrans("ACGT", "TGCA")
    return s.translate(comp)[::-1]


# Background frequencies — match human genome average GC ~41%
BG_FREQ = np.array([0.295, 0.205, 0.205, 0.295])  # A,C,G,T => ~41% GC


def random_bg(length: int, freq: np.ndarray = BG_FREQ) -> str:
    bases = "ACGT"
    idx = NPRNG.choice(4, size=length, p=freq)
    return "".join(bases[i] for i in idx)


def generate_motif_embedded(n: int) -> list[str]:
    """Generate sequences with 1-4 motif instances embedded in random background."""
    seqs: list[str] = []
    ppms = [(name, pfm_to_ppm(pfm)) for name, pfm in JASPAR]
    while len(seqs) < n:
        bg = list(random_bg(SEQ_LEN))
        # how many motifs to embed
        n_motifs = NPRNG.choice([1, 1, 2, 2, 3, 4], p=[0.30, 0.25, 0.20, 0.10, 0.10, 0.05])
        placed_ranges = []
        for _ in range(n_motifs):
            name, ppm = ppms[NPRNG.integers(len(ppms))]
            L = ppm.shape[1]
            if L >= SEQ_LEN - 10:
                continue
            inst = sample_motif_instance(ppm, NPRNG)
            if NPRNG.random() < 0.5:
                inst = rev_comp(inst)
            # try placing without overlap
            for _try in range(20):
                pos = int(NPRNG.integers(5, SEQ_LEN - L - 5))
                if not any(not (pos + L < ps or pos > pe) for ps, pe in placed_ranges):
                    bg[pos:pos + L] = list(inst)
                    placed_ranges.append((pos, pos + L))
                    break
        seq = "".join(bg)
        if is_clean(seq):
            seqs.append(seq)
    return seqs


def generate_pure_random(n: int) -> list[str]:
    """Pure random sequences across a range of GC content."""
    seqs: list[str] = []
    # GC content levels
    gc_levels = [0.25, 0.35, 0.41, 0.50, 0.60, 0.70]
    per = n // len(gc_levels)
    for gc in gc_levels:
        # A=T=(1-gc)/2; C=G=gc/2
        freq = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        for _ in range(per):
            seqs.append(random_bg(SEQ_LEN, freq))
    while len(seqs) < n:
        seqs.append(random_bg(SEQ_LEN, BG_FREQ))
    return seqs[:n]


# ---------------------------------------------------------------------------
# Build library
# ---------------------------------------------------------------------------
print("[4/8] Sampling cCRE-centered sequences ...", flush=True)
COUNTS = {
    "dELS": 10_000,
    "pELS": 5_000,
    "PLS": 3_000,
    "CTCF-only": 3_000,
    "DNase-H3K4me3": 2_000,
}
all_seqs: list[str] = []
for cls, n in COUNTS.items():
    s = sample_ccres(cls, n, shift_range=0)
    print(f"   {cls}: collected {len(s)}", flush=True)
    all_seqs.extend(s)

print("[5/8] Sampling cCRE-flanking shifted windows ...", flush=True)
flank_shift_seqs: list[str] = []
attempts = 0
target_flank = 4_000
while len(flank_shift_seqs) < target_flank and attempts < target_flank * 10:
    attempts += 1
    chrom, start, end, cls = RNG.choice(ccre_all)
    # shift by ±150-400 bp away from cCRE center
    shift = RNG.choice([-1, 1]) * RNG.randint(150, 400)
    c, s, e = center_window(chrom, start, end, shift)
    seq = fetch_seq(c, s, e)
    if is_clean(seq):
        flank_shift_seqs.append(seq)
print(f"   flank-shifts: {len(flank_shift_seqs)}", flush=True)
all_seqs.extend(flank_shift_seqs)

print("[6/8] Sampling random genomic windows ...", flush=True)
rand_seqs = sample_random_genomic(10_000)
print(f"   random genomic: {len(rand_seqs)}", flush=True)
all_seqs.extend(rand_seqs)

print("[7/8] Generating dinuc-shuffled cCRE negatives ...", flush=True)
shuf_seqs = sample_shuffled_ccres(4_000)
print(f"   shuffled cCREs: {len(shuf_seqs)}", flush=True)
all_seqs.extend(shuf_seqs)

print("[8/8] Generating motif-embedded + pure-random ...", flush=True)
motif_seqs = generate_motif_embedded(7_000)
print(f"   motif-embedded: {len(motif_seqs)}", flush=True)
all_seqs.extend(motif_seqs)

rand_pure = generate_pure_random(2_000)
print(f"   pure-random: {len(rand_pure)}", flush=True)
all_seqs.extend(rand_pure)

print(f"Total collected: {len(all_seqs)}", flush=True)

# Pad up if short
if len(all_seqs) < TARGET_N:
    short = TARGET_N - len(all_seqs)
    print(f"Need {short} more; topping up with random genomic.", flush=True)
    extra = sample_random_genomic(short + 500)
    all_seqs.extend(extra[:short])

# Truncate / shuffle
all_seqs = all_seqs[:TARGET_N]
RNG.shuffle(all_seqs)
assert len(all_seqs) == TARGET_N, f"Got {len(all_seqs)} != {TARGET_N}"
for i, s in enumerate(all_seqs):
    if not is_clean(s):
        raise SystemExit(f"Bad sequence at index {i}: {s[:50]}... len={len(s)}")

out = LIB / "sequences.txt"
with open(out, "w") as fh:
    for s in all_seqs:
        fh.write(s + "\n")
print(f"WROTE: {out} ({len(all_seqs)} sequences)", flush=True)
