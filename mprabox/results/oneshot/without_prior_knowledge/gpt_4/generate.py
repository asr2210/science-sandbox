#!/usr/bin/env python3
"""Generate a 50,000-sequence synthetic MPRA training library."""

from __future__ import annotations

import random
from pathlib import Path


SEED = 20260522
N_SEQS = 50_000
LENGTH = 200
OUT = Path(__file__).resolve().parent / "sequences.txt"
META = Path(__file__).resolve().parent / "sequences_meta.tsv"

BASES = "ACGT"
RC = str.maketrans("ACGT", "TGCA")
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
    "AP1": ["TGASTCA", "TGACTCA", "TGAGTCA"],
    "CREB": ["TGACGTCA"],
    "ETS": ["GGAA", "GGAT", "CCGGAAGT"],
    "SP1": ["GGGCGG", "GGGCGGG", "CCGCCC"],
    "KLF": ["CACCC", "GGGTG"],
    "CTCF": ["CCASYAGGKGGCRS"],
    "GATA": ["WGATAR", "GATAA"],
    "FOX": ["RYAAAYA", "TAAACA"],
    "EBOX": ["CACGTG", "CAGCTG", "CACCTG"],
    "NFY": ["CCAAT", "ATTGG"],
    "NRF1": ["TGCGCATGCGCA", "GCGCATGCGC"],
    "YY1": ["CCATNTT", "ACATNTT"],
    "TEAD": ["CATTCCA", "GGAATG"],
    "RUNX": ["TGTGGT", "ACCACA"],
    "SMAD": ["GTCT", "AGAC"],
    "STAT": ["TTCNNNGAA"],
    "IRF": ["GAAANNGAAA", "AANNGAAA"],
    "NFKB": ["GGGRNNYYCC", "GGGACTTTCC"],
    "CEBP": ["RTTGCGYAAY", "TTGCGCAA"],
    "SOX": ["CTTTGTT", "AACAAAG"],
    "OCT": ["ATGCAAAT"],
    "MEF2": ["CTAWWWWTAG"],
    "HOX": ["TAAT", "ATTA"],
    "P53": ["RRRCWWGYYY"],
    "REST": ["CTGTCC"],
    "TATA": ["TATAWAWR", "TATAAA"],
    "INR": ["YYANWYY"],
    "DPE": ["RGWYV"],
    "BRE": ["SSRCGCC"],
}

PAIR_GRAMMARS = [
    ("AP1", "ETS"),
    ("AP1", "CEBP"),
    ("AP1", "TEAD"),
    ("AP1", "NFKB"),
    ("CREB", "AP1"),
    ("ETS", "SP1"),
    ("ETS", "RUNX"),
    ("ETS", "NRF1"),
    ("GATA", "EBOX"),
    ("GATA", "FOX"),
    ("FOX", "SMAD"),
    ("SOX", "OCT"),
    ("STAT", "IRF"),
    ("NFY", "SP1"),
    ("CTCF", "CTCF"),
    ("YY1", "SP1"),
]

MODULES = [
    ["AP1", "ETS", "SP1", "CEBP", "CREB"],
    ["GATA", "EBOX", "RUNX", "ETS", "KLF"],
    ["FOX", "SMAD", "TEAD", "AP1", "HOX"],
    ["STAT", "IRF", "NFKB", "AP1", "CEBP"],
    ["SOX", "OCT", "YY1", "SP1", "EBOX"],
    ["NRF1", "ETS", "NFY", "SP1", "YY1"],
    ["CTCF", "YY1", "REST", "SP1", "KLF"],
]


def revcomp(seq: str) -> str:
    return seq.translate(RC)[::-1]


def expand_iupac(pattern: str, rng: random.Random) -> str:
    return "".join(rng.choice(IUPAC[ch]) for ch in pattern)


def mutate(seq: str, rng: random.Random, rate: float) -> str:
    chars = list(seq)
    for i, ch in enumerate(chars):
        if rng.random() < rate:
            chars[i] = rng.choice([b for b in BASES if b != ch])
    return "".join(chars)


def motif(name: str, rng: random.Random, weakness: float = 0.0, orient: int | None = None) -> str:
    pat = rng.choice(MOTIFS[name])
    seq = expand_iupac(pat, rng)
    if orient is None:
        orient = rng.choice([1, -1])
    if orient < 0:
        seq = revcomp(seq)
    return mutate(seq, rng, weakness)


def background(rng: random.Random, gc: float, cpg: str = "neutral", length: int = LENGTH) -> str:
    seq = []
    prev = ""
    for _ in range(length):
        local_gc = min(0.9, max(0.1, gc + rng.gauss(0, 0.035)))
        if cpg == "island" and prev == "C" and rng.random() < 0.42:
            b = "G"
        elif cpg == "suppressed" and prev == "C" and rng.random() < 0.08:
            b = rng.choice("ACT")
        else:
            b = rng.choice("GC") if rng.random() < local_gc else rng.choice("AT")
        seq.append(b)
        prev = b
    return "".join(seq)


def insert(seq: str, ins: str, pos: int) -> str:
    pos = max(0, min(len(seq) - len(ins), pos))
    return seq[:pos] + ins + seq[pos + len(ins) :]


def choose_gc(rng: random.Random, lo: float = 0.24, hi: float = 0.76) -> float:
    return rng.uniform(lo, hi)


def add_unique(records: list[tuple[str, str]], seen: set[str], family: str, seq: str) -> None:
    if len(seq) != LENGTH or set(seq) - set(BASES):
        raise ValueError(f"bad sequence in {family}")
    if seq in seen:
        return
    seen.add(seq)
    records.append((family, seq))


def make_gc_spectrum(rng: random.Random, i: int) -> str:
    bins = [0.20, 0.26, 0.32, 0.38, 0.44, 0.50, 0.56, 0.62, 0.68, 0.74, 0.80]
    gc = bins[i % len(bins)] + rng.uniform(-0.025, 0.025)
    mode = rng.choices(["neutral", "suppressed", "island"], weights=[6, 3, 1])[0]
    return background(rng, gc, mode)


def make_single_motif(rng: random.Random) -> str:
    gc = choose_gc(rng)
    seq = background(rng, gc, rng.choice(["neutral", "suppressed", "island"]))
    name = rng.choice([k for k in MOTIFS if k not in {"TATA", "INR", "DPE", "BRE"}])
    copies = rng.choices([1, 2, 3], weights=[7, 2, 1])[0]
    occupied = []
    for _ in range(copies):
        m = motif(name, rng, weakness=rng.choice([0.0, 0.05, 0.12, 0.20]))
        for _attempt in range(40):
            pos = rng.randrange(8, LENGTH - len(m) - 8)
            if all(abs(pos - p) > 10 for p in occupied):
                break
        seq = insert(seq, m, pos)
        occupied.append(pos)
    return seq


def make_pair(rng: random.Random) -> str:
    a, b = rng.choice(PAIR_GRAMMARS)
    gc = choose_gc(rng)
    seq = background(rng, gc, rng.choice(["neutral", "suppressed", "island"]))
    ma = motif(a, rng, weakness=rng.choice([0.0, 0.04, 0.10, 0.18]))
    mb = motif(b, rng, weakness=rng.choice([0.0, 0.04, 0.10, 0.18]))
    spacing = rng.choice([0, 1, 2, 3, 5, 8, 10, 13, 16, 21, 32, 48, 64, 96])
    span = len(ma) + spacing + len(mb)
    if span >= LENGTH - 16:
        spacing = max(0, LENGTH - 24 - len(ma) - len(mb))
        span = len(ma) + spacing + len(mb)
    start = rng.randrange(8, LENGTH - span - 8)
    if rng.random() < 0.5:
        seq = insert(seq, ma, start)
        seq = insert(seq, mb, start + len(ma) + spacing)
    else:
        seq = insert(seq, mb, start)
        seq = insert(seq, ma, start + len(mb) + spacing)
    return seq


def make_enhancer_module(rng: random.Random) -> str:
    module = rng.choice(MODULES)
    gc = choose_gc(rng, 0.30, 0.70)
    seq = background(rng, gc, rng.choice(["neutral", "suppressed"]))
    n = rng.randint(3, 8)
    cluster_start = rng.randrange(12, 90)
    cursor = cluster_start + rng.randrange(0, 12)
    for j in range(n):
        name = rng.choice(module)
        m = motif(name, rng, weakness=rng.choice([0.0, 0.03, 0.08, 0.15]))
        if j == 0:
            pos = cursor
        else:
            cursor += rng.choice([4, 6, 8, 10, 12, 16, 21, 34])
            pos = cursor + rng.randrange(-3, 4)
        if pos > LENGTH - len(m) - 8:
            pos = rng.randrange(8, LENGTH - len(m) - 8)
        seq = insert(seq, m, pos)
    return seq


def make_promoter_like(rng: random.Random) -> str:
    seq = background(rng, rng.uniform(0.52, 0.76), rng.choice(["island", "island", "neutral"]))
    if rng.random() < 0.65:
        seq = insert(seq, motif("TATA", rng, weakness=rng.choice([0.0, 0.05, 0.12]), orient=1), rng.randrange(62, 78))
    if rng.random() < 0.85:
        seq = insert(seq, motif("INR", rng, weakness=rng.choice([0.0, 0.08]), orient=1), rng.randrange(95, 106))
    if rng.random() < 0.45:
        seq = insert(seq, motif("DPE", rng, weakness=0.05, orient=1), rng.randrange(122, 139))
    if rng.random() < 0.35:
        seq = insert(seq, motif("BRE", rng, weakness=0.08, orient=1), rng.randrange(52, 68))
    for name in rng.sample(["SP1", "NFY", "ETS", "NRF1", "YY1", "KLF"], rng.randint(2, 5)):
        m = motif(name, rng, weakness=rng.choice([0.0, 0.05, 0.12]))
        pos = rng.choice([rng.randrange(12, 60), rng.randrange(135, 182)])
        seq = insert(seq, m, pos)
    return seq


def make_homotypic(rng: random.Random) -> str:
    name = rng.choice(["AP1", "ETS", "SP1", "GATA", "EBOX", "FOX", "CTCF", "STAT", "IRF", "RUNX", "TEAD"])
    seq = background(rng, choose_gc(rng), rng.choice(["neutral", "suppressed", "island"]))
    copies = rng.randint(2, 7)
    spacing = rng.choice([0, 2, 4, 6, 8, 10, 11, 16, 21, 32])
    motifs = [motif(name, rng, weakness=rng.choice([0.0, 0.04, 0.10, 0.18])) for _ in range(copies)]
    span = sum(len(m) for m in motifs) + spacing * (copies - 1)
    if span > LENGTH - 20:
        return make_enhancer_module(rng)
    pos = rng.randrange(10, LENGTH - span - 10)
    for m in motifs:
        seq = insert(seq, m, pos)
        pos += len(m) + spacing
    return seq


def make_repeat_control(rng: random.Random) -> str:
    kind = rng.choice(["tandem", "poly", "periodic", "shuffled_blocks", "motif_decoy"])
    if kind == "tandem":
        unit = "".join(rng.choice(BASES) for _ in range(rng.choice([2, 3, 4, 5, 6, 8, 10])))
        seq = (unit * ((LENGTH // len(unit)) + 1))[:LENGTH]
        chars = list(seq)
        for i in range(LENGTH):
            if rng.random() < 0.06:
                chars[i] = rng.choice([b for b in BASES if b != chars[i]])
        return "".join(chars)
    if kind == "poly":
        seq = background(rng, choose_gc(rng), "neutral")
        for _ in range(rng.randint(2, 5)):
            run_base = rng.choice(BASES)
            run_len = rng.randint(8, 24)
            seq = insert(seq, run_base * run_len, rng.randrange(0, LENGTH - run_len))
        return seq
    if kind == "periodic":
        left = background(rng, choose_gc(rng), "neutral")
        unit = rng.choice(["AT", "GC", "CA", "GT", "AAT", "CGG", "GATA", "CAG"])
        rep = (unit * 80)[: rng.randint(30, 90)]
        return insert(left, rep, rng.randrange(0, LENGTH - len(rep)))
    if kind == "motif_decoy":
        seq = background(rng, choose_gc(rng), rng.choice(["neutral", "suppressed"]))
        for name in rng.sample(list(MOTIFS), rng.randint(3, 7)):
            if name in {"TATA", "INR", "DPE", "BRE"}:
                continue
            m = motif(name, rng, weakness=0.35)
            seq = insert(seq, m, rng.randrange(8, LENGTH - len(m) - 8))
        return seq
    blocks = [background(rng, choose_gc(rng), "neutral")[j : j + 20] for j in range(0, LENGTH, 20)]
    rng.shuffle(blocks)
    return "".join(blocks)[:LENGTH]


def make_local_composition(rng: random.Random) -> str:
    parts = []
    while sum(map(len, parts)) < LENGTH:
        seg_len = min(rng.randint(18, 55), LENGTH - sum(map(len, parts)))
        parts.append(
            background(
                rng,
                rng.uniform(0.18, 0.84),
                rng.choice(["neutral", "suppressed", "island"]),
                length=seg_len,
            )
        )
    seq = "".join(parts)[:LENGTH]
    for _ in range(rng.randint(0, 3)):
        name = rng.choice(["AP1", "ETS", "SP1", "GATA", "FOX", "EBOX", "NFY", "CTCF"])
        m = motif(name, rng, weakness=rng.choice([0.0, 0.10, 0.20]))
        seq = insert(seq, m, rng.randrange(6, LENGTH - len(m) - 6))
    return seq


def main() -> None:
    rng = random.Random(SEED)
    records: list[tuple[str, str]] = []
    seen: set[str] = set()
    plan = [
        ("gc_spectrum", 6_000, make_gc_spectrum),
        ("single_motif", 6_000, make_single_motif),
        ("motif_pair", 10_000, make_pair),
        ("enhancer_module", 8_000, make_enhancer_module),
        ("promoter_like", 6_000, make_promoter_like),
        ("homotypic_sweep", 5_000, make_homotypic),
        ("repeat_and_decoy", 4_000, make_repeat_control),
        ("local_composition", 5_000, make_local_composition),
    ]

    for family, target, fn in plan:
        start_n = len(records)
        attempts = 0
        while len(records) - start_n < target:
            attempts += 1
            if attempts > target * 20:
                raise RuntimeError(f"too many duplicate/bad attempts for {family}")
            seq = fn(rng, attempts) if family == "gc_spectrum" else fn(rng)
            add_unique(records, seen, family, seq)

    if len(records) != N_SEQS:
        raise RuntimeError(f"expected {N_SEQS}, got {len(records)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(seq for _, seq in records) + "\n")
    META.write_text(
        "index\tfamily\tgc\n"
        + "\n".join(
            f"{i}\t{family}\t{(seq.count('G') + seq.count('C')) / LENGTH:.3f}"
            for i, (family, seq) in enumerate(records)
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
