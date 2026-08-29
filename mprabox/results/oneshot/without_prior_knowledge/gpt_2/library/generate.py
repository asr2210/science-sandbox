#!/usr/bin/env python3
"""Generate a one-shot 50k MPRA design library.

The generator is deterministic and dependency-free. It intentionally mixes
naturalistic sequence statistics with controlled regulatory grammar sweeps.
"""

from __future__ import annotations

import random
from collections import Counter
from pathlib import Path


SEED = 20260522
LENGTH = 200
TARGET = 50_000
OUT = Path(__file__).resolve().parent / "sequences.txt"

IUPAC = {
    "A": "A",
    "C": "C",
    "G": "G",
    "T": "T",
    "R": "AG",
    "Y": "CT",
    "S": "GC",
    "W": "AT",
    "K": "GT",
    "M": "AC",
    "B": "CGT",
    "D": "AGT",
    "H": "ACT",
    "V": "ACG",
    "N": "ACGT",
}

MOTIFS = {
    "AP1": ["TGACTCA", "TGAGTCA"],
    "CRE": ["TGACGTCA"],
    "ETS": ["GGAA", "GGAT"],
    "SP1": ["GGGCGG", "GGGCGGG"],
    "EBOX": ["CACGTG", "CAGCTG", "CATCTG"],
    "NFKB": ["GGGACTTTCC", "GGGAATTTCC"],
    "GATA": ["GATAA", "AGATAAG"],
    "FOX": ["TGTTTAC", "AAACA"],
    "RUNX": ["TGTGGT", "TGTGGC"],
    "CTCF": ["CCCTC", "CCTCCC"],
    "TEAD": ["CATTCCA", "CATTCC"],
    "SMAD": ["GTCTAGAC", "CAGAC"],
    "KLF": ["CACCC", "GGTGGG"],
    "NR": ["AGGTCA", "TGACCT"],
    "MEF2": ["CTAWWWWTAG"],
    "SOX": ["CTTTGTT", "AACAAAG"],
    "POU": ["ATGCAAAT"],
    "P53_HALF": ["RRRCWWGYYY"],
    "TATA": ["TATAWAWR"],
    "INR": ["YYANWYY"],
    "NFY": ["CCAAT"],
    "IRF": ["GAAANNGAAA"],
    "STAT": ["TTCNNNGAA"],
    "RFX": ["GTTRCCNNRGYAAC"],
    "ZEB": ["CACCTG"],
}

MOTIF_NAMES = list(MOTIFS)
CORE_NAMES = [
    "AP1",
    "CRE",
    "ETS",
    "SP1",
    "EBOX",
    "NFKB",
    "GATA",
    "FOX",
    "RUNX",
    "TEAD",
    "SMAD",
    "KLF",
    "NR",
    "SOX",
    "IRF",
    "STAT",
]

PAIRINGS = [
    ("AP1", "ETS"),
    ("AP1", "NFKB"),
    ("AP1", "TEAD"),
    ("CRE", "EBOX"),
    ("CRE", "ETS"),
    ("ETS", "RUNX"),
    ("ETS", "GATA"),
    ("ETS", "IRF"),
    ("SP1", "EBOX"),
    ("SP1", "NFY"),
    ("SP1", "KLF"),
    ("GATA", "FOX"),
    ("GATA", "RUNX"),
    ("FOX", "SOX"),
    ("NR", "NR"),
    ("SMAD", "FOX"),
    ("STAT", "IRF"),
    ("RFX", "ETS"),
    ("CTCF", "SP1"),
    ("TATA", "INR"),
]


def instantiate(pattern: str, rng: random.Random) -> str:
    return "".join(rng.choice(IUPAC[ch]) for ch in pattern)


def revcomp(seq: str) -> str:
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def mutate(seq: str, rate: float, rng: random.Random) -> str:
    chars = list(seq)
    for i, ch in enumerate(chars):
        if rng.random() < rate:
            chars[i] = rng.choice([b for b in "ACGT" if b != ch])
    return "".join(chars)


def motif(name: str, rng: random.Random, strength: float = 1.0) -> str:
    seq = instantiate(rng.choice(MOTIFS[name]), rng)
    if rng.random() < 0.5:
        seq = revcomp(seq)
    if strength < 1.0:
        seq = mutate(seq, (1.0 - strength) * 0.45, rng)
    return seq


def random_bg(length: int, rng: random.Random, gc: float | None = None, cpg: float = 1.0) -> str:
    """Sample a mild first-order background with controllable GC and CpG."""
    if gc is None:
        gc = min(0.78, max(0.22, rng.betavariate(3.0, 3.0)))
    at = (1.0 - gc) / 2.0
    gcp = gc / 2.0
    weights = {"A": at, "T": at, "C": gcp, "G": gcp}
    bases = []
    prev = None
    for _ in range(length):
        local = weights.copy()
        if prev:
            if prev in {"A", "T"}:
                local[prev] *= 1.25
            else:
                local[prev] *= 1.18
            if prev == "C":
                local["G"] *= cpg
        total = sum(local.values())
        x = rng.random() * total
        acc = 0.0
        for base in "ACGT":
            acc += local[base]
            if x <= acc:
                bases.append(base)
                prev = base
                break
    return "".join(bases)


def insert(seq: str, subseq: str, pos: int) -> str:
    return seq[:pos] + subseq + seq[pos + len(subseq) :]


def add_motifs(
    seq: str,
    placements: list[tuple[int, str]],
    rng: random.Random,
    strength: float = 1.0,
) -> str:
    occupied: list[range] = []
    for pos, name in sorted(placements):
        m = motif(name, rng, strength=strength)
        pos = max(0, min(len(seq) - len(m), pos))
        span = range(pos, pos + len(m))
        if any(max(span.start, r.start) < min(span.stop, r.stop) for r in occupied):
            continue
        seq = insert(seq, m, pos)
        occupied.append(span)
    return seq


def dinuc_shuffle(seq: str, rng: random.Random) -> str:
    # A lightweight approximation: shuffle adjacent pairs, preserving many
    # local dinucleotide counts without requiring a graph reconstruction.
    pairs = [seq[i : i + 2] for i in range(0, len(seq) - 1, 2)]
    rng.shuffle(pairs)
    shuffled = "".join(pairs)
    if len(shuffled) < len(seq):
        shuffled += rng.choice("ACGT")
    return shuffled[: len(seq)]


def low_complexity(seq: str, rng: random.Random) -> str:
    chars = list(seq)
    for _ in range(rng.randint(1, 4)):
        start = rng.randrange(0, LENGTH - 20)
        kind = rng.choice(["polyA", "polyT", "CA", "GT", "GC", "AT"])
        if kind == "polyA":
            tract = "A" * rng.randint(8, 22)
        elif kind == "polyT":
            tract = "T" * rng.randint(8, 22)
        else:
            unit = kind
            tract = (unit * rng.randint(5, 14))[: rng.randint(10, 28)]
        chars[start : start + len(tract)] = tract
    return "".join(chars)[:LENGTH]


def gc_of(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq)


def has_bad_run(seq: str) -> bool:
    return any(base * 14 in seq for base in "ACGT")


def valid(seq: str) -> bool:
    return len(seq) == LENGTH and set(seq) <= set("ACGT") and not has_bad_run(seq)


def add(seqs: list[str], seen: set[str], seq: str) -> bool:
    if not valid(seq) or seq in seen:
        return False
    seen.add(seq)
    seqs.append(seq)
    return True


def make_backgrounds(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    while n > 0:
        gc = rng.choice([rng.uniform(0.22, 0.35), rng.uniform(0.35, 0.50), rng.uniform(0.50, 0.65), rng.uniform(0.65, 0.78)])
        cpg = rng.choice([0.25, 0.55, 1.0, 1.6, 2.4])
        seq = random_bg(LENGTH, rng, gc=gc, cpg=cpg)
        if rng.random() < 0.22:
            seq = low_complexity(seq, rng)
        if add(seqs, seen, seq):
            n -= 1


def make_single_motif(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    while n > 0:
        name = rng.choice(MOTIF_NAMES)
        seq = random_bg(LENGTH, rng, gc=rng.uniform(0.30, 0.72), cpg=rng.choice([0.4, 0.8, 1.3, 2.0]))
        placements = []
        for _ in range(rng.choice([1, 1, 1, 2, 3])):
            placements.append((rng.randrange(12, 180), name))
        seq = add_motifs(seq, placements, rng, strength=rng.choice([1.0, 1.0, 0.85, 0.7]))
        if add(seqs, seen, seq):
            n -= 1


def make_clusters(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    while n > 0:
        seq = random_bg(LENGTH, rng, gc=rng.uniform(0.32, 0.70), cpg=rng.choice([0.55, 1.0, 1.8]))
        names = rng.sample(CORE_NAMES, rng.randint(3, 7))
        start = rng.randrange(18, 95)
        placements = []
        pos = start
        for name in names:
            placements.append((pos, name))
            pos += rng.randint(8, 28)
        if rng.random() < 0.35:
            names2 = rng.sample(CORE_NAMES, rng.randint(2, 5))
            pos = rng.randrange(95, 165)
            for name in names2:
                placements.append((pos, name))
                pos += rng.randint(7, 20)
        seq = add_motifs(seq, placements, rng, strength=rng.choice([1.0, 0.9, 0.8]))
        if add(seqs, seen, seq):
            n -= 1


def make_pair_sweeps(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    spacings = [0, 2, 4, 6, 8, 10, 12, 16, 20, 28, 36, 48, 64]
    made = 0
    idx = 0
    while made < n:
        a, b = PAIRINGS[idx % len(PAIRINGS)]
        idx += 1
        spacing = spacings[(idx // len(PAIRINGS)) % len(spacings)]
        gc = [0.32, 0.42, 0.52, 0.62, 0.72][idx % 5]
        seq = random_bg(LENGTH, rng, gc=gc, cpg=[0.45, 0.8, 1.3, 2.2][idx % 4])
        ma = motif(a, rng, strength=[1.0, 0.9, 0.75][idx % 3])
        mb = motif(b, rng, strength=[1.0, 0.9, 0.75][(idx + 1) % 3])
        block = ma + random_bg(spacing, rng, gc=gc) + mb
        if idx % 4 == 0:
            block = revcomp(block)
        pos = rng.randrange(18, LENGTH - len(block) - 18)
        seq = insert(seq, block, pos)
        if add(seqs, seen, seq):
            made += 1


def make_promoters(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    while n > 0:
        gc = rng.choice([rng.uniform(0.55, 0.78), rng.uniform(0.38, 0.55)])
        seq = random_bg(LENGTH, rng, gc=gc, cpg=rng.choice([1.3, 2.0, 3.0]))
        placements = []
        if rng.random() < 0.55:
            placements.append((rng.randrange(42, 76), "TATA"))
            placements.append((rng.randrange(78, 112), "INR"))
        else:
            for _ in range(rng.randint(3, 9)):
                placements.append((rng.randrange(18, 170), rng.choice(["SP1", "KLF", "NFY", "EBOX", "ETS"])))
        if rng.random() < 0.35:
            placements.append((rng.randrange(115, 175), rng.choice(["AP1", "CRE", "NFKB", "NR", "STAT"])))
        seq = add_motifs(seq, placements, rng, strength=rng.choice([1.0, 0.9, 0.8]))
        if add(seqs, seen, seq):
            n -= 1


def make_mutational_series(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    made = 0
    while made < n:
        base = random_bg(LENGTH, rng, gc=rng.uniform(0.35, 0.68), cpg=rng.choice([0.55, 1.0, 1.8]))
        names = rng.sample(CORE_NAMES, 4)
        positions = [38, 72, 112, 148]
        template = add_motifs(base, list(zip(positions, names)), rng, strength=1.0)
        variants = [
            template,
            mutate(template, 0.015, rng),
            mutate(template, 0.04, rng),
            dinuc_shuffle(template, rng),
        ]
        for omit in range(4):
            seq = base
            keep = [(p, nm) for j, (p, nm) in enumerate(zip(positions, names)) if j != omit]
            variants.append(add_motifs(seq, keep, rng, strength=1.0))
        for v in variants:
            if made >= n:
                break
            if add(seqs, seen, v):
                made += 1


def make_negatives(n: int, rng: random.Random, seqs: list[str], seen: set[str]) -> None:
    while n > 0:
        mode = rng.choice(["random", "shuffle", "muted", "extreme_gc"])
        if mode == "random":
            seq = random_bg(LENGTH, rng, gc=rng.uniform(0.25, 0.75), cpg=rng.choice([0.2, 0.5, 1.0]))
        elif mode == "shuffle" and seqs:
            seq = dinuc_shuffle(rng.choice(seqs), rng)
        elif mode == "muted":
            seq = random_bg(LENGTH, rng, gc=rng.uniform(0.35, 0.65), cpg=0.45)
            seq = mutate(seq, 0.08, rng)
        else:
            seq = random_bg(LENGTH, rng, gc=rng.choice([rng.uniform(0.18, 0.28), rng.uniform(0.72, 0.82)]), cpg=rng.choice([0.2, 2.5]))
        if rng.random() < 0.15:
            seq = low_complexity(seq, rng)
        if add(seqs, seen, seq):
            n -= 1


def main() -> None:
    rng = random.Random(SEED)
    seqs: list[str] = []
    seen: set[str] = set()

    strata = [
        ("backgrounds", 7_000, make_backgrounds),
        ("single_motif", 8_000, make_single_motif),
        ("clusters", 11_000, make_clusters),
        ("pair_sweeps", 8_000, make_pair_sweeps),
        ("promoters", 6_000, make_promoters),
        ("mutational_series", 5_000, make_mutational_series),
        ("negatives", 5_000, make_negatives),
    ]
    assert sum(count for _, count, _ in strata) == TARGET

    for _, count, fn in strata:
        fn(count, rng, seqs, seen)

    rng.shuffle(seqs)
    assert len(seqs) == TARGET
    assert len(set(seqs)) == TARGET
    assert all(valid(seq) for seq in seqs)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(seqs) + "\n")

    gcs = [gc_of(seq) for seq in seqs]
    counts = Counter(round(gc, 1) for gc in gcs)
    print(f"wrote {len(seqs)} sequences to {OUT}")
    print(f"GC min/mean/max: {min(gcs):.3f}/{sum(gcs)/len(gcs):.3f}/{max(gcs):.3f}")
    print("rounded GC distribution:", dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
