#!/usr/bin/env python3
"""Generate a 50,000-sequence synthetic MPRA design library."""

from __future__ import annotations

import random
from pathlib import Path


SEED = 6128457
N_SEQUENCES = 50_000
SEQ_LEN = 200
OUT = Path("library/sequences.txt")

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

MOTIFS = [
    ("SP1_GC", "GGGCGG", "ubiquitous"),
    ("KLF", "CACCC", "ubiquitous"),
    ("E2F", "TTTSSCGC", "cell_cycle"),
    ("NRF1", "GCGCATGCGC", "metabolic"),
    ("YY1", "CCATNTT", "architectural"),
    ("CTCF_SHORT", "CCCTC", "architectural"),
    ("CTCF_LONG", "CCASYAGGKGGCRS", "architectural"),
    ("ETS", "GGAA", "signaling"),
    ("ELK", "CCGGAAGT", "signaling"),
    ("AP1", "TGASTCA", "signaling"),
    ("CRE", "TGACGTCA", "signaling"),
    ("ATF_HALF", "TGACG", "signaling"),
    ("NFkB", "GGGRNNYYCC", "immune"),
    ("IRF", "GAAANNGAAA", "immune"),
    ("ISRE", "AGTTTCNNTTTCY", "immune"),
    ("STAT", "TTCNNNGAA", "immune"),
    ("NFKB_HALF", "GGGACT", "immune"),
    ("EBOX_CANON", "CACGTG", "bhlh"),
    ("EBOX_MYC", "CACGTG", "bhlh"),
    ("EBOX_TWIST", "CAGCTG", "bhlh"),
    ("EBOX_TAL", "CAGATG", "bhlh"),
    ("GATA", "WGATAR", "lineage"),
    ("TAL_GATA", "CAGATGG", "lineage"),
    ("RUNX", "TGTGGT", "lineage"),
    ("FOX", "TRTTKRY", "forkhead"),
    ("HNF", "GTTAATNATTAAC", "nuclear_receptor"),
    ("CEBP", "TTGCGCAA", "metabolic"),
    ("HNF4", "RGGNCAAAGKTCAN", "nuclear_receptor"),
    ("RXR_DR1", "AGGTCAAAGGTCA", "nuclear_receptor"),
    ("ER_DR3", "AGGTCANNNTGACCT", "nuclear_receptor"),
    ("GR", "GGTACANNNTGTTCT", "nuclear_receptor"),
    ("PPAR", "AGGTCANAGGTCA", "nuclear_receptor"),
    ("RORA", "AWWNTRGGTCA", "nuclear_receptor"),
    ("SOX", "AACAAT", "development"),
    ("OCT", "ATGCAAAT", "development"),
    ("POU", "ATGCAAATNNNNTAAT", "development"),
    ("NANOG", "TAATGG", "development"),
    ("KLF4", "RGGYGYG", "development"),
    ("ESRRB", "TCAAGGTCA", "development"),
    ("TEAD", "CATTCCA", "development"),
    ("SMAD", "CAGAC", "signaling"),
    ("TCF_LEF", "CTTTGWW", "wnt"),
    ("RBPJ", "TGGGAA", "notch"),
    ("GLI", "GACCACCCA", "hedgehog"),
    ("MEF2", "YTAWWWWTAR", "muscle"),
    ("HAND", "NRTCTG", "development"),
    ("TBX", "AGGTGTGA", "development"),
    ("PAX", "GTCACGCWTSANTGA", "development"),
    ("HOMEZ", "TAATTA", "homeobox"),
    ("HOX", "TAATNN", "homeobox"),
    ("PITX", "TAATCC", "homeobox"),
    ("DLX", "TAATTG", "homeobox"),
    ("NKX", "CAAGTG", "homeobox"),
    ("PBX", "TGATTGAT", "homeobox"),
    ("MEIS", "TGACAG", "homeobox"),
    ("RFX", "GTNRCCNNRGYAAC", "architectural"),
    ("NFI", "TTGGCNNNNNGCCAA", "architectural"),
    ("P53", "RRRCWWGYYYNNRRRCWWGYYY", "stress"),
    ("HIF", "RCGTG", "stress"),
    ("XBP1", "CCACGTCATC", "stress"),
    ("NFE2L2", "TGACTCAGCA", "stress"),
    ("MAF", "TGCTGACTCAGCA", "stress"),
    ("BACH", "TGCTGAGTCAGCA", "stress"),
    ("TATA", "TATAWAAR", "core_promoter"),
    ("INR", "YYANWYY", "core_promoter"),
    ("CCAAT", "CCAAT", "core_promoter"),
    ("BRE", "SSRCGCC", "core_promoter"),
    ("DPE", "RGWYV", "core_promoter"),
    ("POLYA_AATAAA", "AATAAA", "rna_processing"),
]

BY_CLASS = {}
for motif in MOTIFS:
    BY_CLASS.setdefault(motif[2], []).append(motif)


def expand_iupac(pattern: str, rng: random.Random) -> str:
    return "".join(rng.choice(IUPAC[ch]) for ch in pattern)


def rc(seq: str) -> str:
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def maybe_rc(seq: str, rng: random.Random) -> str:
    return rc(seq) if rng.random() < 0.5 else seq


def random_bg(rng: random.Random, gc: float | None = None, length: int = SEQ_LEN) -> str:
    if gc is None:
        gc = rng.choice([0.24, 0.30, 0.36, 0.42, 0.50, 0.58, 0.66, 0.74])
    probs = [("A", (1 - gc) / 2), ("C", gc / 2), ("G", gc / 2), ("T", (1 - gc) / 2)]
    bases = []
    run_base = ""
    run_len = 0
    for _ in range(length):
        x = rng.random()
        acc = 0.0
        base = "T"
        for b, p in probs:
            acc += p
            if x <= acc:
                base = b
                break
        if base == run_base:
            run_len += 1
            if run_len >= 5:
                base = rng.choice([b for b in "ACGT" if b != run_base])
                run_base = base
                run_len = 1
        else:
            run_base = base
            run_len = 1
        bases.append(base)
    return "".join(bases)


def markov_bg(rng: random.Random, gc: float | None = None) -> str:
    if gc is None:
        gc = rng.uniform(0.28, 0.72)
    seq = [rng.choice("ACGT")]
    for _ in range(SEQ_LEN - 1):
        prev = seq[-1]
        if rng.random() < 0.08:
            choices = "CG" if prev in "CG" else "AT"
            seq.append(rng.choice(choices))
        elif prev == "C" and rng.random() < 0.12:
            seq.append("G")
        else:
            seq.append(random_bg(rng, gc, 1))
    return "".join(seq)


def insert(seq: str, motif: str, pos: int) -> str:
    return seq[:pos] + motif + seq[pos + len(motif):]


def nonoverlap_positions(rng: random.Random, lengths: list[int], min_gap: int = 2) -> list[int]:
    for _ in range(200):
        positions = []
        occupied = []
        ok = True
        for length in lengths:
            pos = rng.randrange(4, SEQ_LEN - length - 4)
            if any(not (pos + length + min_gap <= s or pos >= e + min_gap) for s, e in occupied):
                ok = False
                break
            positions.append(pos)
            occupied.append((pos, pos + length))
        if ok:
            return positions
    cursor = 8
    positions = []
    for length in lengths:
        positions.append(cursor)
        cursor += length + min_gap + 4
    return positions


def shuffle_seq(seq: str, rng: random.Random) -> str:
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)


def mutate(seq: str, rng: random.Random, n: int = 2) -> str:
    chars = list(seq)
    for pos in rng.sample(range(len(chars)), min(n, len(chars))):
        chars[pos] = rng.choice([b for b in "ACGT" if b != chars[pos]])
    return "".join(chars)


def sample_motif(rng: random.Random, classes: list[str] | None = None) -> tuple[str, str, str]:
    pool = [m for c in classes for m in BY_CLASS[c]] if classes else MOTIFS
    return rng.choice(pool)


def place_motifs(
    rng: random.Random,
    motifs: list[tuple[str, str, str]],
    gc: float | None = None,
    positions: list[int] | None = None,
    background: str | None = None,
) -> str:
    seq = background or (markov_bg(rng, gc) if rng.random() < 0.35 else random_bg(rng, gc))
    concrete = [maybe_rc(expand_iupac(m[1], rng), rng) for m in motifs]
    if positions is None:
        positions = nonoverlap_positions(rng, [len(m) for m in concrete], rng.choice([1, 2, 4, 8, 12]))
    for motif, pos in sorted(zip(concrete, positions), key=lambda x: x[1]):
        seq = insert(seq, motif, pos)
    return seq


def add_unique(seqs: list[str], seen: set[str], seq: str) -> bool:
    if len(seq) != SEQ_LEN or any(c not in "ACGT" for c in seq) or seq in seen:
        return False
    seen.add(seq)
    seqs.append(seq)
    return True


def fill(seqs: list[str], seen: set[str], target_add: int, maker) -> None:
    target = len(seqs) + target_add
    attempts = 0
    while len(seqs) < target:
        if add_unique(seqs, seen, maker()):
            continue
        attempts += 1
        if attempts > target_add * 50:
            raise RuntimeError("too many duplicate/invalid generation attempts")


def make_backgrounds(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    def maker() -> str:
        if rng.random() < 0.55:
            return random_bg(rng)
        if rng.random() < 0.85:
            return markov_bg(rng)
        base = random_bg(rng, rng.uniform(0.22, 0.78))
        return shuffle_seq(base, rng)

    fill(seqs, seen, n, maker)


def make_singletons(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    def maker() -> str:
        motif = sample_motif(rng)
        gc = rng.choice([0.30, 0.38, 0.46, 0.54, 0.62, 0.70])
        concrete = maybe_rc(expand_iupac(motif[1], rng), rng)
        pos = rng.randrange(8, SEQ_LEN - len(concrete) - 8)
        return place_motifs(rng, [motif], gc=gc, positions=[pos])

    fill(seqs, seen, n, maker)


def make_pairs(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    favored_pairs = [
        (["ubiquitous"], ["signaling"]),
        (["bhlh"], ["lineage"]),
        (["forkhead"], ["nuclear_receptor"]),
        (["immune"], ["signaling"]),
        (["homeobox"], ["development"]),
        (["architectural"], ["ubiquitous"]),
        (["core_promoter"], ["ubiquitous"]),
        (["stress"], ["signaling"]),
    ]

    def maker() -> str:
        c1, c2 = rng.choice(favored_pairs)
        m1 = sample_motif(rng, c1)
        m2 = sample_motif(rng, c2)
        s1 = maybe_rc(expand_iupac(m1[1], rng), rng)
        s2 = maybe_rc(expand_iupac(m2[1], rng), rng)
        spacing = rng.choice([0, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64])
        total = len(s1) + spacing + len(s2)
        start = rng.randrange(6, SEQ_LEN - total - 6)
        if rng.random() < 0.5:
            motifs = [(m1[0], s1, m1[2]), (m2[0], s2, m2[2])]
        else:
            motifs = [(m2[0], s2, m2[2]), (m1[0], s1, m1[2])]
        bg = markov_bg(rng, rng.uniform(0.30, 0.70))
        bg = insert(bg, motifs[0][1], start)
        bg = insert(bg, motifs[1][1], start + len(motifs[0][1]) + spacing)
        return bg

    fill(seqs, seen, n, maker)


def make_triples(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    class_sets = [
        ["ubiquitous", "signaling", "bhlh"],
        ["immune", "signaling", "ubiquitous"],
        ["development", "homeobox", "forkhead"],
        ["nuclear_receptor", "forkhead", "metabolic"],
        ["lineage", "bhlh", "architectural"],
        ["stress", "signaling", "ubiquitous"],
    ]

    def maker() -> str:
        classes = rng.choice(class_sets)
        motifs = [sample_motif(rng, [c]) for c in classes]
        rng.shuffle(motifs)
        return place_motifs(rng, motifs, gc=rng.uniform(0.30, 0.70))

    fill(seqs, seen, n, maker)


def make_homotypic(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    def maker() -> str:
        motif = sample_motif(rng)
        copies = rng.choice([2, 3, 4, 5, 6])
        motifs = [motif] * copies
        return place_motifs(rng, motifs, gc=rng.uniform(0.28, 0.72))

    fill(seqs, seen, n, maker)


def make_promoters(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    tata = BY_CLASS["core_promoter"]
    upstream_classes = ["ubiquitous", "signaling", "nuclear_receptor", "forkhead", "immune"]

    def maker() -> str:
        seq = random_bg(rng, rng.uniform(0.42, 0.68))
        if rng.random() < 0.65:
            seq = insert(seq, maybe_rc(expand_iupac(rng.choice(tata)[1], rng), rng), rng.randrange(72, 108))
        if rng.random() < 0.75:
            inr = expand_iupac("YYANWYY", rng)
            seq = insert(seq, inr, rng.randrange(112, 132))
        for pos in rng.sample(range(16, 76), rng.choice([1, 2, 3])):
            motif = sample_motif(rng, [rng.choice(upstream_classes)])
            concrete = maybe_rc(expand_iupac(motif[1], rng), rng)
            if pos + len(concrete) < 95:
                seq = insert(seq, concrete, pos)
        return seq

    fill(seqs, seen, n, maker)


def make_enhancers(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    classes = [
        "ubiquitous",
        "signaling",
        "immune",
        "bhlh",
        "lineage",
        "forkhead",
        "nuclear_receptor",
        "development",
        "homeobox",
        "stress",
    ]

    def maker() -> str:
        k = rng.choice([4, 5, 6, 7, 8])
        chosen = [sample_motif(rng, [rng.choice(classes)]) for _ in range(k)]
        return place_motifs(rng, chosen, gc=rng.uniform(0.30, 0.68))

    fill(seqs, seen, n, maker)


def make_mutational_contrasts(rng: random.Random, seqs: list[str], seen: set[str], n: int) -> None:
    target = len(seqs) + n
    while len(seqs) < target:
        motif = sample_motif(rng)
        concrete = maybe_rc(expand_iupac(motif[1], rng), rng)
        pos = rng.randrange(12, SEQ_LEN - len(concrete) - 12)
        bg = markov_bg(rng, rng.uniform(0.32, 0.68))
        positive = insert(bg, concrete, pos)
        add_unique(seqs, seen, positive)
        if len(seqs) >= target:
            break
        if rng.random() < 0.5:
            decoy = insert(bg, mutate(concrete, rng, rng.choice([1, 2, 3])), pos)
        else:
            decoy = insert(bg, shuffle_seq(concrete, rng), pos)
        add_unique(seqs, seen, decoy)


def main() -> None:
    rng = random.Random(SEED)
    seqs: list[str] = []
    seen: set[str] = set()

    make_backgrounds(rng, seqs, seen, 8_000)
    make_singletons(rng, seqs, seen, 9_000)
    make_pairs(rng, seqs, seen, 11_000)
    make_triples(rng, seqs, seen, 8_000)
    make_homotypic(rng, seqs, seen, 5_000)
    make_promoters(rng, seqs, seen, 3_500)
    make_enhancers(rng, seqs, seen, 3_500)
    make_mutational_contrasts(rng, seqs, seen, 2_000)

    assert len(seqs) == N_SEQUENCES
    rng.shuffle(seqs)
    assert len(set(seqs)) == N_SEQUENCES
    assert all(len(s) == SEQ_LEN and set(s) <= set("ACGT") for s in seqs)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(seqs) + "\n")


if __name__ == "__main__":
    main()
