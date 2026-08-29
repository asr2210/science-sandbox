#!/usr/bin/env python3
"""Generate a deterministic 50k x 200 bp MPRA training library."""

from __future__ import annotations

import random
from collections import Counter
from pathlib import Path


SEED = 20260527
N_SEQS = 50_000
LENGTH = 200

IUPAC = {
    "A": "A",
    "C": "C",
    "G": "G",
    "T": "T",
    "R": "AG",
    "Y": "CT",
    "S": "CG",
    "W": "AT",
    "K": "GT",
    "M": "AC",
    "B": "CGT",
    "D": "AGT",
    "H": "ACT",
    "V": "ACG",
    "N": "ACGT",
}

COMP = str.maketrans("ACGT", "TGCA")


MOTIFS = [
    # Ubiquitous promoter/enhancer families
    ("SP1_GC", "GGGCGGG", "ubiquitous", 2.3),
    ("KLF_GC", "GGGTGGG", "ubiquitous", 1.8),
    ("ETS", "GGAA", "ubiquitous", 2.1),
    ("ELK_ETS", "CCGGAAGT", "ubiquitous", 1.4),
    ("AP1", "TGASTCA", "signal", 2.2),
    ("CREB", "TGACGTCA", "signal", 1.9),
    ("EBOX", "CACGTG", "ubiquitous", 2.0),
    ("MYC_EBOX", "CACATG", "ubiquitous", 1.3),
    ("NFY_CCAAT", "CCAAT", "promoter", 1.7),
    ("NRF1", "GCGCATGCGC", "promoter", 1.2),
    ("YY1", "CCATNTT", "architectural", 1.2),
    ("CTCF", "CCGCGNGGNGGCAG", "architectural", 1.7),
    ("RFX", "GTTRCCATGGYAAC", "architectural", 1.0),
    ("REST_HALF", "TCAGCACC", "architectural", 0.8),
    # Lineage- and pathway-diverse motifs
    ("GATA", "WGATAR", "lineage", 1.7),
    ("FOXA", "TRTTTRTTT", "lineage", 1.4),
    ("HNF4", "CAAAGTCCA", "lineage", 1.0),
    ("CEBP", "TTGCGCAA", "lineage", 1.3),
    ("RUNX", "TGTGGT", "lineage", 1.2),
    ("PU1_SPI", "AGGAAGTG", "lineage", 1.1),
    ("IRF", "GAAA", "immune", 1.3),
    ("ISRE", "GAAANNGAAA", "immune", 1.0),
    ("NFKB", "GGGRNNYYCC", "immune", 1.3),
    ("STAT", "TTCNNNGAA", "signal", 1.2),
    ("SMAD", "GTCTAGAC", "signal", 0.8),
    ("TEAD", "CATTCCA", "signal", 0.9),
    ("MEF2", "YTAWWWWTAR", "lineage", 0.8),
    ("SOX", "AACAAAG", "lineage", 1.1),
    ("POU", "ATGCAAAT", "lineage", 0.8),
    ("P53", "RRRCWWGYYY", "signal", 0.8),
    ("HIF", "RCGTG", "signal", 1.1),
    ("EGR", "GCGTGGGCG", "signal", 0.9),
    ("TEF_BZIP", "TGAYGTAA", "signal", 0.7),
    ("TAL_GATA", "CAGATG", "lineage", 1.0),
    ("HOMEODOMAIN", "TAATTA", "lineage", 0.9),
]

PROMOTER_MOTIFS = [
    ("TATA", "TATAWAWR", -31, 1.0),
    ("INR", "YYANWYY", 0, 1.4),
    ("DPE", "RGWYV", 30, 0.7),
    ("BRE", "SSRCGCC", -38, 0.5),
    ("CCAAT", "CCAAT", -75, 1.0),
    ("GCBOX", "GGGCGG", -58, 1.5),
    ("ETS_PROM", "GGAA", -47, 0.9),
    ("EBOX_PROM", "CACGTG", -83, 0.8),
]

PAIR_TEMPLATES = [
    ("AP1", "ETS"),
    ("AP1", "IRF"),
    ("ETS", "GATA"),
    ("EBOX", "GATA"),
    ("NFY_CCAAT", "SP1_GC"),
    ("SP1_GC", "ETS"),
    ("CREB", "AP1"),
    ("NFKB", "IRF"),
    ("STAT", "IRF"),
    ("FOXA", "HNF4"),
    ("CEBP", "AP1"),
    ("RUNX", "ETS"),
    ("SOX", "POU"),
    ("CTCF", "YY1"),
]


def rc(seq: str) -> str:
    return seq.translate(COMP)[::-1]


def instantiate(pattern: str, rng: random.Random) -> str:
    return "".join(rng.choice(IUPAC[ch]) for ch in pattern)


def mutate(seq: str, rng: random.Random, n: int = 1) -> str:
    out = list(seq)
    for pos in rng.sample(range(len(out)), min(n, len(out))):
        choices = [b for b in "ACGT" if b != out[pos]]
        out[pos] = rng.choice(choices)
    return "".join(out)


def weighted_choice(items, rng: random.Random):
    total = sum(item[-1] for item in items)
    x = rng.random() * total
    upto = 0.0
    for item in items:
        upto += item[-1]
        if upto >= x:
            return item
    return items[-1]


def choose_gc(rng: random.Random, mode: str) -> float:
    if mode == "cpg":
        return min(0.78, max(0.55, rng.gauss(0.66, 0.055)))
    if mode == "at":
        return min(0.42, max(0.20, rng.gauss(0.32, 0.05)))
    if mode == "balanced":
        return min(0.62, max(0.38, rng.gauss(0.50, 0.06)))
    if mode == "gc":
        return min(0.72, max(0.48, rng.gauss(0.58, 0.06)))
    # Genomic mixture with a long tail toward CpG-rich promoters.
    r = rng.random()
    if r < 0.25:
        return min(0.38, max(0.20, rng.gauss(0.31, 0.04)))
    if r < 0.68:
        return min(0.52, max(0.34, rng.gauss(0.43, 0.045)))
    if r < 0.90:
        return min(0.64, max(0.46, rng.gauss(0.54, 0.045)))
    return min(0.78, max(0.58, rng.gauss(0.66, 0.05)))


def genomic_background(rng: random.Random, mode: str = "genomic") -> str:
    gc = choose_gc(rng, mode)
    at = 1.0 - gc
    base_probs = {"A": at / 2, "T": at / 2, "C": gc / 2, "G": gc / 2}
    cpg_factor = 1.5 if mode == "cpg" else (0.55 if gc < 0.58 else 0.85)
    same_factor = rng.uniform(1.05, 1.45)
    purine_run_factor = rng.uniform(0.85, 1.2)

    seq = [rng.choices("ACGT", [base_probs[b] for b in "ACGT"])[0]]
    for _ in range(1, LENGTH):
        weights = []
        prev = seq[-1]
        for b in "ACGT":
            w = base_probs[b]
            if b == prev:
                w *= same_factor
            if prev == "C" and b == "G":
                w *= cpg_factor
            if prev in "AG" and b in "AG":
                w *= purine_run_factor
            if prev in "CT" and b in "CT":
                w *= purine_run_factor
            weights.append(w)
        seq.append(rng.choices("ACGT", weights)[0])
    return "".join(seq)


def repeat_background(rng: random.Random) -> str:
    motifs = ["CA", "TG", "TA", "AT", "GC", "GAA", "TTC", "CAG", "CTG", "AAT", "TTA"]
    seq = list(genomic_background(rng, rng.choice(["at", "balanced", "gc"])))
    for _ in range(rng.randint(1, 4)):
        unit = rng.choice(motifs)
        copies = rng.randint(5, 24)
        max_len = min(60, len(unit) * copies)
        min_len = min(12, max_len)
        tract = (unit * copies)[: rng.randint(min_len, max_len)]
        pos = rng.randint(0, LENGTH - len(tract))
        seq[pos : pos + len(tract)] = tract
    return "".join(seq)


def random_background(rng: random.Random) -> str:
    if rng.random() < 0.55:
        return "".join(rng.choice("ACGT") for _ in range(LENGTH))
    return genomic_background(rng, rng.choice(["at", "balanced", "gc", "cpg"]))


def can_place(occupied: list[bool], pos: int, n: int, pad: int = 2) -> bool:
    start = max(0, pos - pad)
    end = min(LENGTH, pos + n + pad)
    return not any(occupied[start:end])


def place(seq: list[str], occupied: list[bool], motif: str, pos: int) -> bool:
    if pos < 0 or pos + len(motif) > LENGTH or not can_place(occupied, pos, len(motif)):
        return False
    seq[pos : pos + len(motif)] = motif
    for i in range(pos, pos + len(motif)):
        occupied[i] = True
    return True


def place_random(seq: list[str], occupied: list[bool], motif: str, rng: random.Random) -> bool:
    for _ in range(60):
        pos = rng.randint(8, LENGTH - len(motif) - 8)
        if place(seq, occupied, motif, pos):
            return True
    return False


def motif_by_name(name: str):
    for item in MOTIFS:
        if item[0] == name:
            return item
    raise KeyError(name)


def oriented(pattern: str, rng: random.Random, force_rc: bool | None = None) -> str:
    motif = instantiate(pattern, rng)
    if force_rc is None:
        force_rc = rng.random() < 0.5
    return rc(motif) if force_rc else motif


def enhancer_sequence(rng: random.Random) -> str:
    mode = rng.choices(["genomic", "balanced", "gc", "at", "cpg"], [7, 2, 2, 1, 1])[0]
    seq = list(genomic_background(rng, mode))
    occupied = [False] * LENGTH

    n_motifs = rng.choices([1, 2, 3, 4, 5, 6, 8], [8, 18, 25, 23, 15, 8, 3])[0]
    if rng.random() < 0.45:
        left_name, right_name = rng.choice(PAIR_TEMPLATES)
        left = oriented(motif_by_name(left_name)[1], rng)
        right = oriented(motif_by_name(right_name)[1], rng)
        spacing = rng.choice([4, 6, 8, 10, 12, 16, 20, 25, 32, 40, 55, 70])
        total = len(left) + spacing + len(right)
        start = rng.randint(10, LENGTH - total - 10)
        place(seq, occupied, left, start)
        place(seq, occupied, right, start + len(left) + spacing)
        n_motifs -= 2

    for _ in range(max(0, n_motifs)):
        _, pattern, _, _ = weighted_choice(MOTIFS, rng)
        motif = oriented(pattern, rng)
        if rng.random() < 0.14:
            motif = mutate(motif, rng, rng.choice([1, 1, 2]))
        place_random(seq, occupied, motif, rng)

    return "".join(seq)


def promoter_sequence(rng: random.Random) -> str:
    seq = list(genomic_background(rng, rng.choices(["cpg", "gc", "balanced", "at"], [5, 3, 1, 1])[0]))
    occupied = [False] * LENGTH
    tss = rng.randint(92, 108)

    for _, pattern, rel, weight in PROMOTER_MOTIFS:
        if rng.random() < min(0.95, weight * 0.62):
            motif = oriented(pattern, rng, force_rc=False)
            pos = tss + rel + rng.randint(-5, 5)
            place(seq, occupied, motif, pos)

    for _ in range(rng.choices([1, 2, 3, 4, 5], [10, 22, 28, 25, 15])[0]):
        name, pattern, _, _ = weighted_choice(
            [m for m in MOTIFS if m[2] in {"ubiquitous", "promoter", "signal"}], rng
        )
        motif = oriented(pattern, rng)
        if name in {"SP1_GC", "KLF_GC", "NRF1"} and rng.random() < 0.45:
            pos = rng.randint(25, 120)
            place(seq, occupied, motif, pos)
        else:
            place_random(seq, occupied, motif, rng)

    return "".join(seq)


def architectural_sequence(rng: random.Random) -> str:
    seq = list(genomic_background(rng, rng.choices(["balanced", "gc", "cpg"], [4, 4, 2])[0]))
    occupied = [False] * LENGTH
    motifs = ["CTCF", "YY1", "RFX", "REST_HALF", "SP1_GC", "ETS"]
    for _ in range(rng.choices([2, 3, 4, 5, 6], [10, 25, 30, 22, 13])[0]):
        name = rng.choice(motifs)
        motif = oriented(motif_by_name(name)[1], rng)
        place_random(seq, occupied, motif, rng)
    return "".join(seq)


def perturbation_family(rng: random.Random) -> list[str]:
    bg_mode = rng.choices(["genomic", "balanced", "gc", "cpg", "at"], [4, 2, 2, 1, 1])[0]
    base = list(genomic_background(rng, bg_mode))
    left_name, right_name = rng.choice(PAIR_TEMPLATES)
    left_pattern = motif_by_name(left_name)[1]
    right_pattern = motif_by_name(right_name)[1]
    left = oriented(left_pattern, rng)
    right = oriented(right_pattern, rng)
    spacing = rng.choice([5, 8, 12, 16, 24, 36, 52])
    total = len(left) + spacing + len(right)
    start = rng.randint(12, LENGTH - total - 12)
    variants = []

    def make(lmotif: str, rmotif: str, shift: int = 0, invert_right: bool = False) -> str:
        seq = base.copy()
        occupied = [False] * LENGTH
        place(seq, occupied, lmotif, start)
        r = rc(rmotif) if invert_right else rmotif
        place(seq, occupied, r, start + len(lmotif) + spacing + shift)
        return "".join(seq)

    variants.append(make(left, right))
    variants.append(make(mutate(left, rng, 2), right))
    variants.append(make(left, mutate(right, rng, 2)))
    variants.append(make(left, right, shift=rng.choice([-3, -2, 2, 3]), invert_right=True))
    return variants


def null_sequence(rng: random.Random) -> str:
    if rng.random() < 0.45:
        return random_background(rng)
    if rng.random() < 0.50:
        return repeat_background(rng)
    seq = list(genomic_background(rng, rng.choice(["at", "balanced", "gc", "cpg"])))
    # Add deliberately motif-poor-ish short shuffles by avoiding long consensus insertions.
    for _ in range(rng.randint(2, 7)):
        pos = rng.randint(0, LENGTH - 6)
        seq[pos : pos + 6] = list(instantiate(rng.choice(["AAAAAA", "TTTTTT", "ACACAC", "GTGTGT"]), rng))
    return "".join(seq)


def gc(seq: str) -> float:
    c = Counter(seq)
    return (c["G"] + c["C"]) / len(seq)


def build_library() -> list[str]:
    rng = random.Random(SEED)
    seqs: list[str] = []
    seen: set[str] = set()

    quotas = [
        ("enhancer", 19_000),
        ("promoter", 9_000),
        ("architectural", 5_000),
        ("perturb", 8_000),
        ("null", 9_000),
    ]

    def add(seq: str) -> None:
        if len(seq) != LENGTH or any(b not in "ACGT" for b in seq):
            raise ValueError("invalid sequence")
        if seq not in seen:
            seen.add(seq)
            seqs.append(seq)

    for kind, quota in quotas:
        start_n = len(seqs)
        while len(seqs) - start_n < quota:
            if kind == "enhancer":
                add(enhancer_sequence(rng))
            elif kind == "promoter":
                add(promoter_sequence(rng))
            elif kind == "architectural":
                add(architectural_sequence(rng))
            elif kind == "perturb":
                for seq in perturbation_family(rng):
                    if len(seqs) - start_n < quota:
                        add(seq)
            elif kind == "null":
                add(null_sequence(rng))
            else:
                raise AssertionError(kind)

    rng.shuffle(seqs)
    if len(seqs) != N_SEQS:
        raise AssertionError(len(seqs))
    return seqs


def main() -> None:
    seqs = build_library()
    out = Path(__file__).resolve().parent / "sequences.txt"
    out.write_text("\n".join(seqs) + "\n")

    gcs = [gc(s) for s in seqs]
    print(f"wrote {len(seqs)} sequences to {out}")
    print(f"unique={len(set(seqs))} length={len(seqs[0])} gc_mean={sum(gcs)/len(gcs):.3f}")
    print(f"gc_min={min(gcs):.3f} gc_max={max(gcs):.3f}")


if __name__ == "__main__":
    main()
