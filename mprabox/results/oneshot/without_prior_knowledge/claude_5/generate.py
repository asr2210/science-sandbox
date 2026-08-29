#!/usr/bin/env python3
"""Generate the MPRA training library.

50,000 × 200bp sequences. Composition documented in notebook.md.
"""
import os
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pysam

SEED = 42
LEN = 200
OUT = Path("library/sequences.txt")
DATA = Path("data")
FA = DATA / "hg38.fa"
CCRE = DATA / "ccre_v4.bed"

random.seed(SEED)
np.random.seed(SEED)

# Counts (sum = 50,000)
COUNTS = {
    "PLS": 6500,
    "pELS": 6500,
    "dELS": 16000,
    "CA-CTCF": 3000,
    "CA": 2000,
    "CA-H3K4me3": 2000,
    "CA-TF": 1000,
    "TF": 2000,
    # synthetic / control buckets handled separately
    "random_uniform": 3500,        # 1500 + 2000 extras combined
    "random_varied_gc": 1500,
    "shuffled_ccre": 3000,
    "intergenic": 3000,
}
assert sum(COUNTS.values()) == 50000, sum(COUNTS.values())

CHR_AUTOSOMES = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]


def load_ccre_by_class(bed_path):
    """Return dict: class -> list[(chrom, start, end)]."""
    by_cls = defaultdict(list)
    with open(bed_path) as fh:
        for line in fh:
            parts = line.rstrip().split("\t")
            chrom, s, e = parts[0], int(parts[1]), int(parts[2])
            cls = parts[5]
            if chrom not in CHR_AUTOSOMES:
                continue
            by_cls[cls].append((chrom, s, e))
    return by_cls


def center_200(start, end):
    """Return (s, e) of a 200bp window centred on the cCRE midpoint."""
    mid = (start + end) // 2
    return mid - LEN // 2, mid - LEN // 2 + LEN


def stratified_sample(elements, n, rng):
    """Sample n elements, stratified ~uniformly across chromosomes.

    Within each chromosome we take min(per_chrom_quota, available) and
    top up uniformly at random for any shortfall.
    """
    by_chr = defaultdict(list)
    for el in elements:
        by_chr[el[0]].append(el)

    chroms = sorted(by_chr.keys())
    quota = max(1, n // len(chroms))
    picked = []
    leftover = []
    for c in chroms:
        items = by_chr[c]
        rng.shuffle(items)
        picked.extend(items[:quota])
        leftover.extend(items[quota:])

    if len(picked) > n:
        rng.shuffle(picked)
        picked = picked[:n]
    elif len(picked) < n:
        rng.shuffle(leftover)
        picked.extend(leftover[: n - len(picked)])
    return picked[:n]


VALID = set("ACGT")


def fetch_clean(fa, chrom, s, e):
    """Return uppercase sequence or None if it contains N / out of bounds."""
    if s < 0:
        return None
    try:
        seq = fa.fetch(chrom, s, e).upper()
    except (KeyError, ValueError):
        return None
    if len(seq) != LEN:
        return None
    if any(b not in VALID for b in seq):
        return None
    return seq


def dinuc_shuffle(seq, rng):
    """Altschul-Erickson dinucleotide-shuffle. Preserves dinucleotide composition."""
    # Build graph of dinucleotide edges; do an Eulerian walk.
    # Simple implementation following Altschul & Erickson 1985.
    if len(seq) < 2:
        return seq
    edges = defaultdict(list)
    for i in range(len(seq) - 1):
        edges[seq[i]].append(seq[i + 1])

    # Random shuffle of out-edges; ensure a valid Eulerian path exists by
    # the standard trick: for each node != last_char, randomly pick one
    # outgoing edge to designate as "last" so it leads to last_char.
    last = seq[-1]
    # For Altschul-Erickson we need to ensure there's an Eulerian path
    # from seq[0] to seq[-1]. We retry on failure.
    for _ in range(100):
        e = {k: v[:] for k, v in edges.items()}
        for v in e.values():
            rng.shuffle(v)
        # walk
        out = [seq[0]]
        cur = seq[0]
        ok = True
        for _ in range(len(seq) - 1):
            if not e[cur]:
                ok = False
                break
            nxt = e[cur].pop()
            out.append(nxt)
            cur = nxt
        if ok and len(out) == len(seq):
            return "".join(out)
    # fallback: mononucleotide shuffle
    s = list(seq)
    rng.shuffle(s)
    return "".join(s)


def random_seq(length, gc, rng):
    """Random ACGT sequence with target GC fraction."""
    # P(G)=P(C)=gc/2, P(A)=P(T)=(1-gc)/2
    p = [(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2]
    bases = rng.choices("ACGT", weights=p, k=length)
    return "".join(bases)


def main():
    print("[generate] loading cCRE bed ...")
    by_cls = load_ccre_by_class(CCRE)
    for cls, els in by_cls.items():
        print(f"  {cls}: {len(els):,}")

    print("[generate] opening hg38 ...")
    if not (DATA / "hg38.fa.fai").exists():
        pysam.faidx(str(FA))
    fa = pysam.FastaFile(str(FA))

    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)

    seen = set()
    sequences = []

    def add(seq, tag):
        if seq is None:
            return False
        if len(seq) != LEN:
            return False
        if any(b not in VALID for b in seq):
            return False
        if seq in seen:
            return False
        seen.add(seq)
        sequences.append((seq, tag))
        return True

    # ----- cCRE-derived sequences -----
    for cls in ["PLS", "pELS", "dELS", "CA-CTCF", "CA", "CA-H3K4me3", "CA-TF", "TF"]:
        want = COUNTS[cls]
        # oversample to handle Ns / duplicates
        pool = stratified_sample(by_cls.get(cls, []), min(want * 3, len(by_cls.get(cls, []))), rng)
        added = 0
        for chrom, s, e in pool:
            ws, we = center_200(s, e)
            seq = fetch_clean(fa, chrom, ws, we)
            if add(seq, f"ccre_{cls}"):
                added += 1
                if added >= want:
                    break
        # top up if short
        if added < want:
            # full-pool fallback
            extra = by_cls.get(cls, [])[:]
            rng.shuffle(extra)
            for chrom, s, e in extra:
                if added >= want:
                    break
                ws, we = center_200(s, e)
                seq = fetch_clean(fa, chrom, ws, we)
                if add(seq, f"ccre_{cls}"):
                    added += 1
        print(f"[generate] {cls}: added {added}/{want}")
        assert added == want, f"{cls} short: {added}/{want}"

    # ----- dinucleotide-shuffled cCREs -----
    # Use a balanced mix of cCRE classes as source for shuffling.
    shuf_sources = []
    for cls in ["PLS", "pELS", "dELS", "CA-CTCF", "TF"]:
        shuf_sources.extend(stratified_sample(by_cls.get(cls, []), 1500, rng))
    rng.shuffle(shuf_sources)
    added = 0
    for chrom, s, e in shuf_sources:
        ws, we = center_200(s, e)
        seq = fetch_clean(fa, chrom, ws, we)
        if seq is None:
            continue
        shuffled = dinuc_shuffle(seq, rng)
        if add(shuffled, "shuffled_ccre"):
            added += 1
            if added >= COUNTS["shuffled_ccre"]:
                break
    print(f"[generate] shuffled_ccre: added {added}/{COUNTS['shuffled_ccre']}")
    assert added == COUNTS["shuffled_ccre"]

    # ----- Intergenic genomic background (>5kb from any cCRE) -----
    # Build per-chrom sorted cCRE intervals
    chr_intervals = defaultdict(list)
    for cls, els in by_cls.items():
        for chrom, s, e in els:
            chr_intervals[chrom].append((s, e))
    for c in chr_intervals:
        chr_intervals[c].sort()

    chrom_lens = {c: fa.get_reference_length(c) for c in CHR_AUTOSOMES}
    want = COUNTS["intergenic"]
    added = 0
    attempts = 0
    max_attempts = want * 100
    # weight chromosome sampling by length
    chr_pop = list(chrom_lens.keys())
    chr_w = np.array([chrom_lens[c] for c in chr_pop], dtype=float)
    chr_w /= chr_w.sum()
    while added < want and attempts < max_attempts:
        attempts += 1
        c = nprng.choice(chr_pop, p=chr_w)
        L = chrom_lens[c]
        s = int(nprng.integers(0, L - LEN))
        e = s + LEN
        # check distance to nearest cCRE on this chrom (binary search)
        ivs = chr_intervals[c]
        # use bisect on starts
        import bisect
        starts = [iv[0] for iv in ivs]
        idx = bisect.bisect_left(starts, s)
        too_close = False
        for j in (idx - 1, idx):
            if 0 <= j < len(ivs):
                cs, ce = ivs[j]
                if not (e + 5000 < cs or s - 5000 > ce):
                    too_close = True
                    break
        if too_close:
            continue
        seq = fetch_clean(fa, c, s, e)
        if add(seq, "intergenic"):
            added += 1
    print(f"[generate] intergenic: added {added}/{want}")
    assert added == want, f"intergenic short: {added}/{want}"

    # ----- Random uniform GC=50% -----
    want = COUNTS["random_uniform"]
    added = 0
    while added < want:
        seq = random_seq(LEN, 0.5, rng)
        if add(seq, "random_uniform"):
            added += 1
    print(f"[generate] random_uniform: added {added}/{want}")

    # ----- Random varied GC (30-70%) -----
    want = COUNTS["random_varied_gc"]
    added = 0
    gcs = nprng.uniform(0.30, 0.70, size=want * 3)
    gi = 0
    while added < want:
        gc = float(gcs[gi % len(gcs)])
        gi += 1
        seq = random_seq(LEN, gc, rng)
        if add(seq, "random_varied_gc"):
            added += 1
    print(f"[generate] random_varied_gc: added {added}/{want}")

    print(f"[generate] total sequences: {len(sequences)}")
    assert len(sequences) == 50000, len(sequences)

    # shuffle final order so class blocks don't bias any split prepare.py does
    rng.shuffle(sequences)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as fh:
        for seq, _tag in sequences:
            fh.write(seq + "\n")
    print(f"[generate] wrote {OUT}")

    # composition report
    from collections import Counter
    tags = Counter(t for _, t in sequences)
    print("[generate] composition:")
    for t, n in sorted(tags.items(), key=lambda kv: -kv[1]):
        print(f"  {t}: {n}")


if __name__ == "__main__":
    main()
