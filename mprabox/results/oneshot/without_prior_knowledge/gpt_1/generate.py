#!/usr/bin/env python3
"""Generate a 50k x 200 bp MPRA training library.

The design intentionally mixes real TF motif profiles with synthetic
backgrounds and perturbations.  It is deterministic and validates the final
contract before writing library/sequences.txt.
"""

from __future__ import annotations

import math
import random
import re
from collections import defaultdict
from pathlib import Path


SEED = 20260522
N_SEQS = 50_000
LENGTH = 200
BASES = "ACGT"
RC = str.maketrans("ACGT", "TGCA")


def revcomp(seq: str) -> str:
    return seq.translate(RC)[::-1]


def weighted_choice(rng: random.Random, items, weights):
    total = sum(weights)
    x = rng.random() * total
    acc = 0.0
    for item, weight in zip(items, weights):
        acc += weight
        if acc >= x:
            return item
    return items[-1]


class Motif:
    def __init__(self, mid: str, name: str, counts: dict[str, list[int]]):
        self.mid = mid
        self.name = name
        self.counts = counts
        self.length = len(counts["A"])
        self.ppm = []
        self.consensus = []
        self.ic = 0.0
        for i in range(self.length):
            col = [counts[b][i] + 0.5 for b in BASES]
            total = sum(col)
            probs = [c / total for c in col]
            self.ppm.append(probs)
            self.consensus.append(BASES[max(range(4), key=lambda j: probs[j])])
            entropy = -sum(p * math.log2(p) for p in probs)
            self.ic += 2.0 - entropy
        self.consensus = "".join(self.consensus)
        self.score = max(0.01, self.ic / max(1, self.length))
        self.family = infer_family(name)

    def sample(self, rng: random.Random, strength: str = "normal") -> str:
        out = []
        for probs in self.ppm:
            if strength == "strong":
                adjusted = [p**1.7 for p in probs]
            elif strength == "weak":
                adjusted = [p**0.55 for p in probs]
            else:
                adjusted = probs
            out.append(weighted_choice(rng, BASES, adjusted))
        seq = "".join(out)
        if rng.random() < 0.5:
            seq = revcomp(seq)
        return seq


def infer_family(name: str) -> str:
    upper = name.upper()
    patterns = [
        ("bHLH", ["ARNT", "MYC", "MAX", "USF", "TFE", "MITF", "ASCL", "NEURO", "HIF", "BHLH"]),
        ("bZIP", ["JUN", "FOS", "ATF", "CEBP", "CREB", "MAF", "NFE2", "BACH", "BATF", "XBP"]),
        ("ETS", ["ETS", "ELF", "ERG", "FLI", "GABPA", "SPI", "ETV"]),
        ("homeobox", ["HOX", "PAX", "POU", "LHX", "DLX", "NKX", "MEIS", "PBX", "OTX"]),
        ("sox", ["SOX"]),
        ("nuclear_receptor", ["RXR", "RARA", "ESR", "NR", "PPAR", "VDR", "THR", "RORA", "HNF4"]),
        ("forkhead", ["FOX"]),
        ("zinc_finger", ["KLF", "SP", "ZNF", "CTCF", "EGR", "GLI", "WT1"]),
        ("smad_tbox", ["SMAD", "TBX", "EOMES"]),
        ("stat_irf", ["STAT", "IRF", "ISRE"]),
        ("rel", ["REL", "NFKB"]),
        ("gata", ["GATA"]),
        ("runx", ["RUNX"]),
        ("p53", ["TP53", "P53"]),
    ]
    for family, keys in patterns:
        if any(k in upper for k in keys):
            return family
    return "other"


def parse_jaspar(path: Path) -> list[Motif]:
    motifs: list[Motif] = []
    if not path.exists():
        return motifs
    current = None
    counts: dict[str, list[int]] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current and set(counts) == set(BASES):
                motifs.append(Motif(current[0], current[1], counts))
            parts = line[1:].split("\t", 1)
            current = (parts[0], parts[1] if len(parts) > 1 else parts[0])
            counts = {}
        else:
            base = line[0]
            nums = [int(x) for x in re.findall(r"\d+", line)]
            counts[base] = nums
    if current and set(counts) == set(BASES):
        motifs.append(Motif(current[0], current[1], counts))
    return [m for m in motifs if 6 <= m.length <= 24 and m.ic >= 3.5]


def fallback_motifs() -> list[Motif]:
    consensuses = {
        "AP1": "TGACTCA",
        "CRE": "TGACGTCA",
        "CEBP": "TTGCGCAA",
        "EBOX": "CACGTG",
        "HIF": "ACGTG",
        "ETS": "GGAA",
        "GATA": "GATAA",
        "RUNX": "TGTGGT",
        "NFKB": "GGGRNNYYCC".replace("R", "A").replace("N", "A").replace("Y", "C"),
        "CTCF": "CCGCGNGGNGGCAG".replace("N", "A"),
        "SP1": "GGGCGG",
        "KLF": "CACCC",
        "SOX": "AACAAAG",
        "FOX": "TRTTTAC".replace("R", "A"),
        "SMAD": "CAGAC",
        "STAT": "TTCNNNGAA".replace("N", "A"),
        "IRF": "GAAANNGAAA".replace("N", "A"),
        "NR": "AGGTCA",
        "P53": "RRRCWWGYYY".replace("R", "A").replace("W", "A").replace("Y", "C"),
    }
    motifs = []
    for name, seq in consensuses.items():
        counts = {b: [] for b in BASES}
        for c in seq:
            for b in BASES:
                counts[b].append(30 if b == c else 1)
        motifs.append(Motif(name, name, counts))
    return motifs


def make_background(rng: random.Random, gc: float, mode: str = "iid") -> list[str]:
    if mode == "cpg":
        seq = []
        prev = ""
        for _ in range(LENGTH):
            weights = {
                "A": (1 - gc) / 2,
                "T": (1 - gc) / 2,
                "C": gc / 2,
                "G": gc / 2,
            }
            if prev == "C":
                weights["G"] *= 2.2
            if prev == "G":
                weights["C"] *= 1.35
            b = weighted_choice(rng, BASES, [weights[x] for x in BASES])
            seq.append(b)
            prev = b
        return seq
    if mode == "at_patchy":
        seq = []
        local_gc = gc
        for i in range(LENGTH):
            if i % rng.randint(18, 45) == 0:
                local_gc = min(0.75, max(0.18, rng.gauss(gc, 0.13)))
            seq.append(weighted_choice(rng, BASES, [(1 - local_gc) / 2, local_gc / 2, local_gc / 2, (1 - local_gc) / 2]))
        return seq
    return [weighted_choice(rng, BASES, [(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2]) for _ in range(LENGTH)]


def place(seq: list[str], insert: str, pos: int) -> bool:
    if pos < 0 or pos + len(insert) > len(seq):
        return False
    seq[pos : pos + len(insert)] = insert
    return True


def mutate_motif(rng: random.Random, motif_seq: str, rate: float = 0.35) -> str:
    chars = list(motif_seq)
    n = max(1, round(len(chars) * rate))
    for i in rng.sample(range(len(chars)), n):
        chars[i] = rng.choice([b for b in BASES if b != chars[i]])
    return "".join(chars)


def choose_motif(rng: random.Random, motifs: list[Motif], family: str | None = None) -> Motif:
    pool = [m for m in motifs if family is None or m.family == family]
    if not pool:
        pool = motifs
    weights = [0.4 + min(2.5, m.score) for m in pool]
    return weighted_choice(rng, pool, weights)


def insert_motifs(
    rng: random.Random,
    seq: list[str],
    motifs: list[Motif],
    count: int,
    families: list[str] | None = None,
    clustered: bool = False,
    strength: str = "normal",
    allow_overlap: bool = False,
):
    occupied: list[tuple[int, int]] = []
    center = rng.randint(45, 155)
    for i in range(count):
        family = rng.choice(families) if families else None
        motif = choose_motif(rng, motifs, family)
        inst = motif.sample(rng, strength)
        for _ in range(50):
            if clustered:
                pos = int(rng.gauss(center, 25))
            else:
                pos = rng.randint(5, LENGTH - len(inst) - 5)
            pos = max(0, min(LENGTH - len(inst), pos))
            if allow_overlap or all(pos + len(inst) + 2 < a or pos - 2 > b for a, b in occupied):
                place(seq, inst, pos)
                occupied.append((pos, pos + len(inst)))
                break


def promoter_like(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    gc = rng.uniform(0.50, 0.78)
    seq = make_background(rng, gc, "cpg")
    if rng.random() < 0.55:
        place(seq, "TATAWA".replace("W", rng.choice("AT")), rng.randint(55, 90))
    if rng.random() < 0.65:
        place(seq, "YYANWYY".replace("Y", rng.choice("CT")).replace("W", rng.choice("AT")).replace("N", rng.choice(BASES)), rng.randint(88, 112))
    for _ in range(rng.randint(1, 4)):
        place(seq, rng.choice(["GGGCGG", "CCGCCC", "GGCGGG", "GCCGCC"]), rng.randint(8, 180))
    if rng.random() < 0.45:
        place(seq, rng.choice(["CCAAT", "ATTGG", "TTGCGCAA"]), rng.randint(15, 150))
    fams = ["zinc_finger", "ETS", "bHLH", "bZIP", "rel"]
    insert_motifs(rng, seq, motifs, rng.randint(1, 4), fams, clustered=False, strength="weak")
    if variant % 7 == 0:
        # Deliberately weak/noisy promoter controls: keep CpG structure but break
        # several motif cores.
        for _ in range(3):
            pos = rng.randint(0, LENGTH - 8)
            place(seq, mutate_motif(rng, "".join(seq[pos : pos + 8]), 0.5), pos)
    return "".join(seq)


def enhancer_cluster(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    gc = rng.uniform(0.34, 0.66)
    seq = make_background(rng, gc, rng.choice(["iid", "at_patchy"]))
    grammar_sets = [
        ["bZIP", "ETS", "gata", "runx"],
        ["bHLH", "homeobox", "smad_tbox"],
        ["nuclear_receptor", "forkhead", "bZIP"],
        ["stat_irf", "rel", "bZIP"],
        ["zinc_finger", "ETS", "bHLH"],
        ["homeobox", "sox", "forkhead"],
    ]
    families = rng.choice(grammar_sets)
    insert_motifs(rng, seq, motifs, rng.randint(3, 8), families, clustered=True, strength=rng.choice(["weak", "normal", "strong"]))
    if variant % 5 == 0:
        # Add homotypic clusters to teach copy number and saturation.
        fam = rng.choice(families)
        insert_motifs(rng, seq, motifs, rng.randint(2, 5), [fam], clustered=True, strength="strong")
    return "".join(seq)


def syntax_series(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    gc = rng.choice([0.30, 0.38, 0.45, 0.52, 0.60, 0.68])
    seq = make_background(rng, gc, rng.choice(["iid", "at_patchy", "cpg"]))
    if variant % 4 == 0:
        motif = choose_motif(rng, motifs)
        inst = motif.sample(rng, "strong")
        spacing = rng.choice([0, 2, 5, 10, 20, 40])
        start = rng.randint(20, max(21, LENGTH - 2 * len(inst) - spacing - 20))
        place(seq, inst, start)
        place(seq, inst if rng.random() < 0.5 else revcomp(inst), start + len(inst) + spacing)
    elif variant % 4 == 1:
        fam = rng.choice(["bZIP", "bHLH", "ets", "homeobox", "nuclear_receptor", "zinc_finger", "forkhead"])
        insert_motifs(rng, seq, motifs, rng.randint(2, 7), [fam], clustered=False, strength="normal")
    elif variant % 4 == 2:
        insert_motifs(rng, seq, motifs, rng.randint(2, 6), None, clustered=False, strength="normal")
    else:
        insert_motifs(rng, seq, motifs, rng.randint(5, 12), None, clustered=True, strength="weak", allow_overlap=True)
    return "".join(seq)


def perturbation(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    gc = rng.uniform(0.32, 0.70)
    seq = make_background(rng, gc, rng.choice(["iid", "cpg", "at_patchy"]))
    n = rng.randint(2, 5)
    inserted: list[tuple[int, str]] = []
    for _ in range(n):
        motif = choose_motif(rng, motifs)
        inst = motif.sample(rng, "strong")
        pos = rng.randint(10, LENGTH - len(inst) - 10)
        place(seq, inst, pos)
        inserted.append((pos, inst))
    # Mutate a controlled subset so the collection contains matched-like
    # activity gradients without relying on duplicated sequences.
    for pos, inst in inserted[: max(1, variant % (n + 1))]:
        if rng.random() < 0.75:
            place(seq, mutate_motif(rng, inst, rng.uniform(0.25, 0.55)), pos)
    return "".join(seq)


def composition_control(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    gc = [0.20, 0.27, 0.34, 0.42, 0.50, 0.58, 0.66, 0.74, 0.80][variant % 9]
    mode = ["iid", "at_patchy", "cpg"][variant % 3]
    seq = make_background(rng, gc, mode)
    if variant % 11 == 0:
        repeat = rng.choice(["CA", "GT", "GATA", "CAG", "CGG", "AAT"])
        start = rng.randint(0, LENGTH - 60)
        tract = (repeat * ((rng.randint(18, 58) // len(repeat)) + 1))[: rng.randint(18, 58)]
        place(seq, tract, start)
    if variant % 13 == 0:
        # Palindromic/structured controls probe model robustness to local
        # reverse-complement symmetry.
        k = rng.randint(8, 22)
        arm = "".join(make_background(rng, gc, "iid")[:k])
        place(seq, arm + revcomp(arm), rng.randint(5, LENGTH - 2 * k - 5))
    if variant % 5 == 0:
        insert_motifs(rng, seq, motifs, 1, None, clustered=False, strength="weak")
    return "".join(seq)


def motif_panel(rng: random.Random, motifs: list[Motif], variant: int) -> str:
    # One or two interpretable motif families per sequence, intentionally
    # balanced across known TF structural families.
    families = sorted(set(m.family for m in motifs))
    fam1 = families[variant % len(families)]
    fam2 = families[(variant * 7 + 3) % len(families)]
    gc = rng.uniform(0.30, 0.72)
    seq = make_background(rng, gc, "iid")
    insert_motifs(rng, seq, motifs, rng.randint(2, 4), [fam1], clustered=rng.random() < 0.5, strength="strong")
    if rng.random() < 0.65:
        insert_motifs(rng, seq, motifs, rng.randint(1, 3), [fam2], clustered=rng.random() < 0.5, strength="normal")
    return "".join(seq)


def quality_ok(seq: str) -> bool:
    if len(seq) != LENGTH or any(b not in BASES for b in seq):
        return False
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    if not 0.15 <= gc <= 0.85:
        return False
    for b in BASES:
        if b * 18 in seq:
            return False
    return True


def main() -> None:
    rng = random.Random(SEED)
    motifs = parse_jaspar(Path("data/jaspar2024_vertebrates_pfms.txt")) or fallback_motifs()
    # Keep high-information motifs but preserve family breadth by sampling from
    # all acceptable PFMs.  The broad JASPAR non-redundant set is small enough
    # for direct use.
    family_counts = defaultdict(int)
    for m in motifs:
        family_counts[m.family] += 1
    print(f"Loaded {len(motifs)} motifs across {len(family_counts)} inferred families")

    quotas = [
        ("promoter_like", 8_500, promoter_like),
        ("enhancer_cluster", 10_500, enhancer_cluster),
        ("syntax_series", 12_000, syntax_series),
        ("perturbation", 7_500, perturbation),
        ("composition_control", 6_500, composition_control),
        ("motif_panel", 5_000, motif_panel),
    ]
    assert sum(q for _, q, _ in quotas) == N_SEQS

    out: list[str] = []
    seen: set[str] = set()
    category_counts: dict[str, int] = {}
    for name, quota, fn in quotas:
        made = 0
        attempts = 0
        while made < quota:
            attempts += 1
            if attempts > quota * 50:
                raise RuntimeError(f"Could not fill category {name}")
            seq = fn(rng, motifs, made + attempts)
            if not quality_ok(seq) or seq in seen:
                continue
            seen.add(seq)
            out.append(seq)
            made += 1
        category_counts[name] = made

    assert len(out) == N_SEQS
    assert len(set(out)) == N_SEQS
    assert all(quality_ok(s) for s in out)

    out_path = Path("library/sequences.txt")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text("\n".join(out) + "\n")

    print(category_counts)
    gcs = [(s.count("G") + s.count("C")) / LENGTH for s in out]
    print(f"Wrote {len(out)} sequences to {out_path}")
    print(f"GC mean={sum(gcs)/len(gcs):.3f} min={min(gcs):.3f} max={max(gcs):.3f}")


if __name__ == "__main__":
    main()
