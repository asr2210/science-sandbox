#!/usr/bin/env python3
"""Generate the one-shot MPRA library.

The design intentionally avoids prepare.py. It uses external hg38 regulatory
annotations downloaded into data/ and writes exactly 50,000 200 bp sequences.
"""

from __future__ import annotations

import gzip
import json
import math
import os
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "library" / "sequences.txt"
RNG = random.Random(20260527)
DNA = "ACGT"
CANON = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
CANON_SET = set(CANON)


CCRE_QUOTAS = {
    "dELS": 500,
    "pELS": 500,
    "PLS": 500,
    "CA-H3K4me3": 500,
    "CA-CTCF": 500,
    "CA-TF": 500,
    "TF": 500,
    "CA": 500,
}
DHSS_PER_COMPONENT = 2625
TFBS_QUOTA = 1500
MOTIF_SYNTH_QUOTA = 1500
RANDOM_GENOMIC_QUOTA = 500
IID_RANDOM_QUOTA = 500
TOTAL = 50000


MOTIFS = [
    "TGACTCA",  # AP-1
    "TGAATCA",
    "GGGCGG",  # SP/KLF
    "CCGCCC",
    "CACGTG",  # bHLH / MYC-like E-box
    "CAGCTG",
    "GGAA",  # ETS
    "GGAAGT",
    "GATAA",
    "AGATAA",
    "TTCNNNGAA".replace("N", "A"),  # IRF-like concrete seed
    "TTCCGGGAA",
    "AATTA",  # homeobox-like
    "TAATTA",
    "ACAAAG",  # FOX-like
    "TRTTTAC".replace("R", "A"),
    "CTCF",  # replaced below with a CTCF-like consensus fragment
    "CAGGTG",
    "TTGCGCAA",  # NRF1-like
    "GCGCATGCGC",
    "GGGTCA",  # nuclear receptor half-site
    "AGGTCA",
    "TGGGGA",  # NF-kB-like
    "GGGRNNYYCC".replace("R", "A").replace("N", "G").replace("Y", "C"),
]
MOTIFS = ["CCGCGNGGNGGCAG".replace("N", "A") if m == "CTCF" else m for m in MOTIFS]


class Fasta:
    def __init__(self, path: Path):
        self.path = path
        self.index_path = path.with_suffix(path.suffix + ".fai.json")
        self.index = self._load_or_build_index()
        self.handle = open(path, "rb")

    def _load_or_build_index(self) -> dict[str, dict[str, int]]:
        if self.index_path.exists():
            return json.loads(self.index_path.read_text())

        index: dict[str, dict[str, int]] = {}
        with open(self.path, "rb") as fh:
            name = None
            length = 0
            seq_offset = 0
            line_bases = 0
            line_bytes = 0
            while True:
                pos = fh.tell()
                line = fh.readline()
                if not line:
                    if name is not None:
                        index[name] = {
                            "length": length,
                            "offset": seq_offset,
                            "line_bases": line_bases,
                            "line_bytes": line_bytes,
                        }
                    break
                if line.startswith(b">"):
                    if name is not None:
                        index[name] = {
                            "length": length,
                            "offset": seq_offset,
                            "line_bases": line_bases,
                            "line_bytes": line_bytes,
                        }
                    name = line[1:].split()[0].decode("ascii")
                    length = 0
                    seq_offset = fh.tell()
                    line_bases = 0
                    line_bytes = 0
                else:
                    stripped = line.rstrip(b"\r\n")
                    if line_bases == 0:
                        line_bases = len(stripped)
                        line_bytes = len(line)
                    length += len(stripped)

        self.index_path.write_text(json.dumps(index, sort_keys=True))
        return index

    def fetch(self, chrom: str, start: int, end: int) -> str | None:
        meta = self.index.get(chrom)
        if meta is None or start < 0 or end > meta["length"] or end <= start:
            return None
        line_bases = meta["line_bases"]
        line_bytes = meta["line_bytes"]
        offset = meta["offset"]
        pieces = []
        pos = start
        while pos < end:
            line_no, in_line = divmod(pos, line_bases)
            take = min(end - pos, line_bases - in_line)
            self.handle.seek(offset + line_no * line_bytes + in_line)
            pieces.append(self.handle.read(take))
            pos += take
        seq = b"".join(pieces).decode("ascii").upper()
        if len(seq) != end - start or any(base not in DNA for base in seq):
            return None
        return seq


def rc(seq: str) -> str:
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def center_window(record: tuple[str, int, int], fasta: Fasta, jitter: int = 0) -> str | None:
    chrom, start, end = record
    center = (start + end) // 2 + jitter
    return fasta.fetch(chrom, center - 100, center + 100)


def add_sequence(seqs: list[str], seen: set[str], seq: str | None) -> bool:
    if seq is None or len(seq) != 200 or seq in seen:
        return False
    gc = (seq.count("G") + seq.count("C")) / 200
    if gc < 0.18 or gc > 0.82:
        return False
    run = 1
    for prev, cur in zip(seq, seq[1:]):
        run = run + 1 if cur == prev else 1
        if run > 20:
            return False
    seen.add(seq)
    seqs.append(seq)
    return True


def load_dhs_component_sequences() -> dict[int, list[tuple[float, str]]]:
    path = DATA / "train_all_classifier_light.csv.gz"
    per_component: dict[int, list[tuple[float, str]]] = defaultdict(list)
    with gzip.open(path, "rt") as fh:
        header = next(fh).rstrip("\n").split("\t")
        raw_i = header.index("raw_sequence")
        comp_i = header.index("component")
        signal_i = header.index("total_signal")
        samples_i = header.index("numsamples")
        prop_i = header.index("proportion")
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            seq = parts[raw_i].upper()
            comp = int(parts[comp_i])
            signal = float(parts[signal_i])
            samples = int(parts[samples_i])
            proportion = float(parts[prop_i])
            score = (math.log1p(signal) + 0.25) * math.sqrt(samples + 1) * (0.25 + proportion)
            per_component[comp].append((score, seq))
    return per_component


def weighted_sample_without_replacement(records: list[tuple[float, str]], n: int) -> list[str]:
    keyed = []
    for weight, seq in records:
        weight = max(weight, 1e-6)
        keyed.append((math.log(RNG.random()) / weight, seq))
    keyed.sort(reverse=True)
    return [seq for _, seq in keyed[:n]]


def add_dhs_sequences(seqs: list[str], seen: set[str]) -> None:
    per_component = load_dhs_component_sequences()
    for comp in range(1, 17):
        chosen = weighted_sample_without_replacement(per_component[comp], DHSS_PER_COMPONENT * 2)
        added = 0
        for seq in chosen:
            if add_sequence(seqs, seen, seq):
                added += 1
                if added == DHSS_PER_COMPONENT:
                    break
        if added != DHSS_PER_COMPONENT:
            raise RuntimeError(f"Could not fill DHS component {comp}: added {added}")


def load_ccres() -> dict[str, list[tuple[str, int, int]]]:
    records: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    with open(DATA / "GRCh38-cCREs.bed") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            chrom, start_s, end_s, cls = parts[0], parts[1], parts[2], parts[5]
            if chrom not in CANON_SET:
                continue
            start, end = int(start_s), int(end_s)
            if end - start >= 40 and cls in CCRE_QUOTAS:
                records[cls].append((chrom, start, end))
    return records


def add_ccres(seqs: list[str], seen: set[str], fasta: Fasta) -> None:
    records = load_ccres()
    for cls, quota in CCRE_QUOTAS.items():
        pool = records[cls]
        RNG.shuffle(pool)
        added = 0
        attempts = 0
        i = 0
        while added < quota:
            chrom, start, end = pool[i % len(pool)]
            i += 1
            attempts += 1
            jitter = RNG.randint(-35, 35)
            seq = center_window((chrom, start, end), fasta, jitter)
            if add_sequence(seqs, seen, seq):
                added += 1
            if attempts > quota * 20:
                raise RuntimeError(f"Could not fill cCRE quota for {cls}")


def load_tfbs() -> dict[str, list[tuple[str, int, int]]]:
    per_tf: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)
    with gzip.open(DATA / "encRegTfbsClustered.txt.gz", "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 7:
                continue
            chrom = parts[1]
            if chrom not in CANON_SET:
                continue
            start, end = int(parts[2]), int(parts[3])
            name = parts[4]
            score = int(parts[5])
            source_count = int(parts[6])
            if score < 800 or source_count < 2 or end <= start:
                continue
            counts[name] += 1
            record = (chrom, start, end)
            bucket = per_tf[name]
            if len(bucket) < 3000:
                bucket.append(record)
            else:
                j = RNG.randrange(counts[name])
                if j < 3000:
                    bucket[j] = record
    return per_tf


def add_tfbs(seqs: list[str], seen: set[str], fasta: Fasta) -> None:
    per_tf = load_tfbs()
    names = [name for name, pool in per_tf.items() if pool]
    for pool in per_tf.values():
        RNG.shuffle(pool)
    RNG.shuffle(names)
    cursors = {name: 0 for name in names}
    added = 0
    attempts = 0
    while added < TFBS_QUOTA:
        for name in names:
            pool = per_tf[name]
            if not pool:
                continue
            idx = cursors[name] % len(pool)
            cursors[name] += 1
            chrom, start, end = pool[idx]
            jitter = RNG.randint(-25, 25)
            seq = center_window((chrom, start, end), fasta, jitter)
            attempts += 1
            if add_sequence(seqs, seen, seq):
                added += 1
                if added >= TFBS_QUOTA:
                    break
        if attempts > TFBS_QUOTA * 40:
            raise RuntimeError("Could not fill TFBS quota")


def random_gc_background(gc: float) -> str:
    seq = []
    p_gc = max(0.25, min(0.75, gc))
    for _ in range(200):
        if RNG.random() < p_gc:
            seq.append("G" if RNG.random() < 0.5 else "C")
        else:
            seq.append("A" if RNG.random() < 0.5 else "T")
    return "".join(seq)


def add_motif_synth(seqs: list[str], seen: set[str]) -> None:
    added = 0
    while added < MOTIF_SYNTH_QUOTA:
        gc = RNG.betavariate(3, 3) * 0.5 + 0.25
        bases = list(random_gc_background(gc))
        motif_count = RNG.choice([2, 3, 3, 4, 5])
        occupied: list[tuple[int, int]] = []
        for _ in range(motif_count):
            motif = RNG.choice(MOTIFS)
            if RNG.random() < 0.5:
                motif = rc(motif)
            for _try in range(50):
                pos = RNG.randint(8, 192 - len(motif))
                if all(pos + len(motif) <= a or pos >= b for a, b in occupied):
                    bases[pos : pos + len(motif)] = motif
                    occupied.append((pos, pos + len(motif)))
                    break
        if add_sequence(seqs, seen, "".join(bases)):
            added += 1


def add_random_genomic(seqs: list[str], seen: set[str], fasta: Fasta) -> None:
    lengths = {chrom: fasta.index[chrom]["length"] for chrom in CANON if chrom in fasta.index}
    chroms = list(lengths)
    weights = [lengths[c] for c in chroms]
    added = 0
    while added < RANDOM_GENOMIC_QUOTA:
        chrom = RNG.choices(chroms, weights=weights, k=1)[0]
        start = RNG.randint(0, lengths[chrom] - 200)
        seq = fasta.fetch(chrom, start, start + 200)
        if add_sequence(seqs, seen, seq):
            added += 1


def add_iid_random(seqs: list[str], seen: set[str]) -> None:
    added = 0
    while added < IID_RANDOM_QUOTA:
        seq = "".join(RNG.choice(DNA) for _ in range(200))
        if add_sequence(seqs, seen, seq):
            added += 1


def main() -> None:
    fasta_path = DATA / "hg38.fa"
    if not fasta_path.exists():
        raise SystemExit("Missing data/hg38.fa; download and decompress hg38.fa.gz first.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fasta = Fasta(fasta_path)
    seqs: list[str] = []
    seen: set[str] = set()

    add_dhs_sequences(seqs, seen)
    add_ccres(seqs, seen, fasta)
    add_tfbs(seqs, seen, fasta)
    add_motif_synth(seqs, seen)
    add_random_genomic(seqs, seen, fasta)
    add_iid_random(seqs, seen)

    if len(seqs) != TOTAL:
        raise RuntimeError(f"Expected {TOTAL} sequences, got {len(seqs)}")
    if any(len(seq) != 200 or any(base not in DNA for base in seq) for seq in seqs):
        raise RuntimeError("Sequence validation failed")

    OUT.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {OUT}")


if __name__ == "__main__":
    main()
