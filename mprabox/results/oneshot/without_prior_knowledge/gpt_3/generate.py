#!/usr/bin/env python3
"""Generate a 50,000 sequence MPRA design library.

The design is intentionally self contained and deterministic. It mixes broad
sequence-background coverage with motif syntax experiments for many regulatory
TF families, promoter-like elements, and matched perturbation-style examples.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random


SEED = 732451
N_SEQS = 50_000
LENGTH = 200
OUT = Path("library/sequences.txt")

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

RC = str.maketrans("ACGT", "TGCA")


@dataclass(frozen=True)
class Motif:
    name: str
    family: str
    pattern: str
    weight: float = 1.0


MOTIFS = [
    Motif("AP1", "signal", "TGASTCA", 1.6),
    Motif("CREB", "signal", "TGACGTCA", 1.4),
    Motif("ATF", "signal", "TGACGTMA", 1.0),
    Motif("NFkB", "immune", "GGGRNNYYCC", 1.4),
    Motif("IRF", "immune", "GAAA", 1.1),
    Motif("STAT", "immune", "TTCNNNGAA", 1.2),
    Motif("ETS", "hematopoietic", "GGAA", 1.5),
    Motif("RUNX", "hematopoietic", "TGTGGT", 1.2),
    Motif("GATA", "hematopoietic", "WGATAR", 1.4),
    Motif("TAL_EBOX", "hematopoietic", "CAGSTG", 1.0),
    Motif("CEBP", "liver_immune", "TTGCGYAA", 1.3),
    Motif("HNF4_DR1", "nuclear_receptor", "RGGTCAAAGGTCA", 1.0),
    Motif("NR_HALF", "nuclear_receptor", "AGGTCA", 1.0),
    Motif("FOXA", "pioneer", "TRTTKRY", 1.3),
    Motif("HNF1", "liver", "GTTAATNATTAAC", 0.9),
    Motif("SOX", "neural_pioneer", "AACAAAG", 1.2),
    Motif("POU", "neural_pioneer", "ATGCAAAT", 1.0),
    Motif("NEUROD_EBOX", "neural", "CAGATG", 1.0),
    Motif("ASCL_EBOX", "neural", "CAGCTG", 1.0),
    Motif("REST_HALF", "neural_repressor", "TCAGCACC", 0.8),
    Motif("SP1", "promoter", "GGGCGG", 1.5),
    Motif("KLF", "promoter", "CACCC", 1.2),
    Motif("E2F", "cell_cycle", "TTTSSCGC", 1.0),
    Motif("NFY_CCAAT", "promoter", "CCAAT", 1.1),
    Motif("TATA", "promoter", "TATAWAWR", 1.0),
    Motif("INR", "promoter", "YYANWYY", 1.0),
    Motif("CTCF", "architectural", "CCASYAGGTGGCRCY", 1.0),
    Motif("YY1", "architectural", "CCATNTT", 0.9),
    Motif("P53_HALF", "stress", "RRRCWWGYYY", 1.0),
    Motif("TEAD", "signal", "GGAATG", 0.9),
    Motif("SMAD", "signal", "GTCT", 0.8),
    Motif("MEF2", "muscle_neural", "CTAWWWWTAG", 0.8),
    Motif("HOX", "development", "TAAT", 1.0),
    Motif("PAX", "development", "GTCACGCWTSANTGA", 0.7),
    Motif("RFX", "structural", "GTNRCCNNRGYAAC", 0.8),
    Motif("NRF1", "metabolic", "TGCGCATGCGCA", 0.8),
    Motif("NFE2", "erythroid", "TGACTCAGCA", 0.9),
    Motif("MAF", "signal", "TGCTGASTCA", 0.9),
    Motif("BACH", "repressor", "TGCTGAGTCA", 0.8),
    Motif("GRHL", "epithelial", "AACCGGTT", 0.7),
]

PROMOTER_MOTIFS = [m for m in MOTIFS if m.family == "promoter"]
GENERAL_MOTIFS = [m for m in MOTIFS if m.family != "promoter"]

COUNTS = {
    "background": 7_000,
    "single": 7_000,
    "homotypic": 9_000,
    "heterotypic": 14_000,
    "promoter": 6_000,
    "perturbation": 5_000,
    "decoy": 2_000,
}


def sample_iupac(pattern: str, rng: random.Random) -> str:
    return "".join(rng.choice(IUPAC[ch]) for ch in pattern)


def revcomp(seq: str) -> str:
    return seq.translate(RC)[::-1]


def weighted_choice(items: list[Motif], rng: random.Random) -> Motif:
    total = sum(m.weight for m in items)
    x = rng.random() * total
    acc = 0.0
    for item in items:
        acc += item.weight
        if x <= acc:
            return item
    return items[-1]


def random_base(gc: float, rng: random.Random) -> str:
    if rng.random() < gc:
        return rng.choice("GC")
    return rng.choice("AT")


def iid_background(gc: float, rng: random.Random, length: int = LENGTH) -> str:
    return "".join(random_base(gc, rng) for _ in range(length))


def markov_background(gc: float, rng: random.Random, length: int = LENGTH) -> str:
    """First-order-ish DNA with variable run length and composition."""
    seq = [random_base(gc, rng)]
    stay = rng.uniform(0.48, 0.78)
    for _ in range(1, length):
        prev_gc = seq[-1] in "GC"
        if rng.random() < stay:
            seq.append(rng.choice("GC" if prev_gc else "AT"))
        else:
            seq.append(random_base(gc, rng))
    return "".join(seq)


def cpg_background(gc: float, rng: random.Random, length: int = LENGTH) -> str:
    seq = list(iid_background(gc, rng, length))
    mode = rng.choice(["deplete", "neutral", "enrich"])
    if mode == "deplete":
        for i in range(length - 1):
            if seq[i] == "C" and seq[i + 1] == "G" and rng.random() < 0.85:
                seq[i + 1] = rng.choice("ACT")
    elif mode == "enrich":
        for _ in range(rng.randint(4, 18)):
            pos = rng.randrange(length - 1)
            seq[pos : pos + 2] = ["C", "G"]
    return "".join(seq)


def low_complexity_background(gc: float, rng: random.Random, length: int = LENGTH) -> str:
    seq = list(markov_background(gc, rng, length))
    for _ in range(rng.randint(2, 6)):
        run_len = rng.randint(4, 13)
        pos = rng.randrange(0, length - run_len + 1)
        base = random_base(gc, rng)
        if rng.random() < 0.35:
            tract = "".join(rng.choice("AT") for _ in range(run_len))
        else:
            tract = base * run_len
        seq[pos : pos + run_len] = list(tract)
    return "".join(seq)


def background(rng: random.Random, length: int = LENGTH) -> str:
    gc = min(0.82, max(0.18, rng.betavariate(2.0, 2.0) * 0.7 + 0.15))
    mode = rng.choices(
        [iid_background, markov_background, cpg_background, low_complexity_background],
        weights=[0.35, 0.30, 0.25, 0.10],
        k=1,
    )[0]
    return mode(gc, rng, length)


def can_place(occupied: list[tuple[int, int]], start: int, end: int, min_gap: int = 0) -> bool:
    for a, b in occupied:
        if start < b + min_gap and end + min_gap > a:
            return False
    return True


def embed(seq: str, insert: str, rng: random.Random, occupied: list[tuple[int, int]] | None = None,
          pos: int | None = None, min_gap: int = 1) -> tuple[str, tuple[int, int]]:
    occupied = occupied if occupied is not None else []
    ins = insert if rng.random() < 0.5 else revcomp(insert)
    if pos is not None:
        start = max(0, min(len(seq) - len(ins), pos))
        if not can_place(occupied, start, start + len(ins), min_gap=0):
            raise ValueError("requested occupied motif placement")
    else:
        for _ in range(200):
            start = rng.randrange(0, len(seq) - len(ins) + 1)
            if can_place(occupied, start, start + len(ins), min_gap=min_gap):
                break
        else:
            start = rng.randrange(0, len(seq) - len(ins) + 1)
    chars = list(seq)
    chars[start : start + len(ins)] = list(ins)
    return "".join(chars), (start, start + len(ins))


def mutate_interval(seq: str, interval: tuple[int, int], rng: random.Random) -> str:
    chars = list(seq)
    start, end = interval
    for i in range(start, end):
        choices = [b for b in "ACGT" if b != chars[i]]
        chars[i] = rng.choice(choices)
    return "".join(chars)


def shuffled_decoy(seq: str, rng: random.Random) -> str:
    chars = list(seq)
    for block_start in range(0, len(chars), 10):
        block = chars[block_start : block_start + 10]
        rng.shuffle(block)
        chars[block_start : block_start + 10] = block
    return "".join(chars)


def make_background(rng: random.Random) -> str:
    return background(rng)


def make_single(rng: random.Random) -> str:
    seq = background(rng)
    motif = weighted_choice(MOTIFS, rng)
    site = sample_iupac(motif.pattern, rng)
    if rng.random() < 0.25:
        site = weaken_site(site, rng)
    seq, _ = embed(seq, site, rng)
    return seq


def make_homotypic(rng: random.Random) -> str:
    seq = background(rng)
    motif = weighted_choice(GENERAL_MOTIFS + PROMOTER_MOTIFS, rng)
    occupied: list[tuple[int, int]] = []
    copies = rng.choices([2, 3, 4, 5, 6, 7, 8], weights=[8, 10, 9, 6, 4, 2, 1], k=1)[0]
    for _ in range(copies):
        site = sample_iupac(motif.pattern, rng)
        if rng.random() < 0.20:
            site = weaken_site(site, rng)
        seq, interval = embed(seq, site, rng, occupied=occupied, min_gap=rng.randint(1, 12))
        occupied.append(interval)
    return seq


def make_heterotypic(rng: random.Random) -> str:
    seq = background(rng)
    occupied: list[tuple[int, int]] = []
    families = list({m.family for m in MOTIFS})
    rng.shuffle(families)
    n = rng.choices([3, 4, 5, 6, 7, 8, 9], weights=[4, 8, 10, 8, 5, 3, 1], k=1)[0]
    chosen: list[Motif] = []
    for fam in families:
        fam_motifs = [m for m in MOTIFS if m.family == fam]
        if fam_motifs:
            chosen.append(weighted_choice(fam_motifs, rng))
        if len(chosen) == n:
            break
    while len(chosen) < n:
        chosen.append(weighted_choice(MOTIFS, rng))
    for motif in chosen:
        site = sample_iupac(motif.pattern, rng)
        if rng.random() < 0.12:
            site = weaken_site(site, rng)
        seq, interval = embed(seq, site, rng, occupied=occupied, min_gap=rng.randint(0, 10))
        occupied.append(interval)
    return seq


def make_promoter(rng: random.Random) -> str:
    seq = cpg_background(rng.uniform(0.48, 0.72), rng)
    occupied: list[tuple[int, int]] = []
    layout = [
        ("TATAWAWR", rng.randint(45, 72), 0.55),
        ("YYANWYY", rng.randint(84, 104), 0.75),
        ("CCAAT", rng.randint(25, 55), 0.45),
        ("GGGCGG", rng.randint(20, 90), 0.75),
        ("CACCC", rng.randint(20, 120), 0.50),
    ]
    for pattern, pos, prob in layout:
        if rng.random() < prob:
            site = sample_iupac(pattern, rng)
            try:
                seq, interval = embed(seq, site, rng, occupied=occupied, pos=pos, min_gap=1)
                occupied.append(interval)
            except ValueError:
                pass
    for _ in range(rng.randint(1, 4)):
        motif = weighted_choice(GENERAL_MOTIFS, rng)
        seq, interval = embed(seq, sample_iupac(motif.pattern, rng), rng, occupied=occupied, min_gap=5)
        occupied.append(interval)
    return seq


def weaken_site(site: str, rng: random.Random) -> str:
    chars = list(site)
    n = 1 if len(chars) < 8 else rng.choice([1, 1, 2])
    for i in rng.sample(range(len(chars)), n):
        choices = [b for b in "ACGT" if b != chars[i]]
        chars[i] = rng.choice(choices)
    return "".join(chars)


def make_perturbation_batch(rng: random.Random) -> list[str]:
    motif = weighted_choice(MOTIFS, rng)
    base = background(rng)
    occupied: list[tuple[int, int]] = []
    site = sample_iupac(motif.pattern, rng)
    base, interval = embed(base, site, rng, occupied=occupied, min_gap=2)
    occupied.append(interval)
    partner = weighted_choice([m for m in MOTIFS if m.family != motif.family] or MOTIFS, rng)
    if rng.random() < 0.65:
        partner_site = sample_iupac(partner.pattern, rng)
        pos = max(0, min(LENGTH - len(partner_site), interval[1] + rng.choice([4, 8, 12, 20, 35])))
        try:
            base, p_interval = embed(base, partner_site, rng, occupied=occupied, pos=pos, min_gap=1)
            occupied.append(p_interval)
        except ValueError:
            pass
    mutated = mutate_interval(base, interval, rng)
    weakened = list(base)
    weak = weaken_site(base[interval[0] : interval[1]], rng)
    weakened[interval[0] : interval[1]] = list(weak)
    flipped_site = revcomp(base[interval[0] : interval[1]])
    flipped = list(base)
    flipped[interval[0] : interval[1]] = list(flipped_site)
    return [base, mutated, "".join(weakened), "".join(flipped)]


def make_decoy(rng: random.Random) -> str:
    seq = make_heterotypic(rng) if rng.random() < 0.6 else make_homotypic(rng)
    return shuffled_decoy(seq, rng)


def add_unique(seqs: list[str], seen: set[str], candidate: str) -> bool:
    if len(candidate) != LENGTH:
        raise ValueError(f"bad length {len(candidate)}")
    if any(ch not in "ACGT" for ch in candidate):
        raise ValueError("bad alphabet")
    if candidate in seen:
        return False
    seen.add(candidate)
    seqs.append(candidate)
    return True


def fill_category(name: str, target: int, maker, rng: random.Random,
                  seqs: list[str], seen: set[str]) -> None:
    start = len(seqs)
    attempts = 0
    while len(seqs) - start < target:
        attempts += 1
        if attempts > target * 100:
            raise RuntimeError(f"too many duplicate attempts in {name}")
        candidate = maker(rng)
        add_unique(seqs, seen, candidate)


def main() -> None:
    rng = random.Random(SEED)
    seqs: list[str] = []
    seen: set[str] = set()

    fill_category("background", COUNTS["background"], make_background, rng, seqs, seen)
    fill_category("single", COUNTS["single"], make_single, rng, seqs, seen)
    fill_category("homotypic", COUNTS["homotypic"], make_homotypic, rng, seqs, seen)
    fill_category("heterotypic", COUNTS["heterotypic"], make_heterotypic, rng, seqs, seen)
    fill_category("promoter", COUNTS["promoter"], make_promoter, rng, seqs, seen)

    while len(seqs) < sum(COUNTS[k] for k in ("background", "single", "homotypic", "heterotypic", "promoter", "perturbation")):
        for candidate in make_perturbation_batch(rng):
            if len(seqs) >= sum(COUNTS[k] for k in ("background", "single", "homotypic", "heterotypic", "promoter", "perturbation")):
                break
            add_unique(seqs, seen, candidate)

    fill_category("decoy", COUNTS["decoy"], make_decoy, rng, seqs, seen)

    if len(seqs) != N_SEQS:
        raise RuntimeError(f"generated {len(seqs)} sequences, expected {N_SEQS}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {OUT}")


if __name__ == "__main__":
    main()
