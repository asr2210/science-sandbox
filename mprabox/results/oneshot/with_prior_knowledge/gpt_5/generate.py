#!/usr/bin/env python3
"""
Generate a 50,000-sequence MPRA design.

The design is mostly public hg38 DHS summit-centered sequence, sampled by NMF
topic loading, with smaller control strata for shuffled DHS grammar, flanking
genomic sequence, and GC-stratified synthetic DNA.
"""

from __future__ import annotations

import gzip
import os
import random
import struct
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "library" / "sequences.txt"
N_TOTAL = 50_000
SEED = 130913

DHS_PATH = DATA / "DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
MIX_PATH = DATA / "2018-06-08NC16_NNDSVD_Mixture.npy.gz"
TWOBIT_PATH = DATA / "hg38.2bit"


class TwoBit:
    def __init__(self, path: Path):
        self.path = path
        self.fh = open(path, "rb")
        sig = self.fh.read(4)
        if sig == struct.pack(">I", 0x1A412743):
            self.endian = ">"
        elif sig == struct.pack("<I", 0x1A412743):
            self.endian = "<"
        else:
            raise ValueError("not a 2bit file")
        version, seq_count, _reserved = self._read("III")
        if version != 0:
            raise ValueError(f"unsupported 2bit version {version}")
        self.index = {}
        for _ in range(seq_count):
            name_len = self.fh.read(1)[0]
            name = self.fh.read(name_len).decode("ascii")
            (offset,) = self._read("I")
            self.index[name] = offset

    def _read(self, fmt: str):
        size = struct.calcsize(self.endian + fmt)
        return struct.unpack(self.endian + fmt, self.fh.read(size))

    def sequence(self, chrom: str) -> str:
        self.fh.seek(self.index[chrom])
        dna_size, = self._read("I")
        n_count, = self._read("I")
        n_starts = list(self._read(f"{n_count}I")) if n_count else []
        n_sizes = list(self._read(f"{n_count}I")) if n_count else []
        mask_count, = self._read("I")
        if mask_count:
            self.fh.seek(8 * mask_count, os.SEEK_CUR)
        self.fh.seek(4, os.SEEK_CUR)
        packed = self.fh.read((dna_size + 3) // 4)

        bases = [""] * (len(packed) * 4)
        alphabet = ("T", "C", "A", "G")
        j = 0
        for byte in packed:
            bases[j] = alphabet[(byte >> 6) & 3]
            bases[j + 1] = alphabet[(byte >> 4) & 3]
            bases[j + 2] = alphabet[(byte >> 2) & 3]
            bases[j + 3] = alphabet[byte & 3]
            j += 4
        seq = bases[:dna_size]
        for start, size in zip(n_starts, n_sizes):
            seq[start:start + size] = "N" * size
        return "".join(seq)


def load_mixture_weights() -> np.ndarray:
    with gzip.open(MIX_PATH, "rb") as handle:
        mix = np.load(handle)
    # Sum over NMF topics to mimic topic-loading weighted DHS sampling, then
    # damp the most ubiquitous/high-signal tail so no single topic dominates.
    weights = mix.sum(axis=0)
    weights = np.sqrt(np.maximum(weights, 0))
    weights += 1e-8
    return weights / weights.sum()


def weighted_indices(weights: np.ndarray, count: int, rng: np.random.Generator) -> set[int]:
    # Oversample then unique-filter; all draws are row indices in the DHS table.
    chosen: set[int] = set()
    need = count
    while len(chosen) < count:
        draw = rng.choice(len(weights), size=max(need * 2, 1024), replace=False, p=weights)
        chosen.update(int(x) for x in draw)
        need = count - len(chosen)
    return set(list(chosen)[:count])


def read_selected_dhs(indices: set[int]) -> list[dict[str, object]]:
    rows = []
    with gzip.open(DHS_PATH, "rt") as handle:
        header = next(handle).rstrip("\n").split("\t")
        pos = {name: i for i, name in enumerate(header)}
        for row_i, line in enumerate(handle):
            if row_i not in indices:
                continue
            parts = line.rstrip("\n").split("\t")
            rows.append(
                {
                    "chrom": parts[pos["seqname"]],
                    "start": int(parts[pos["start"]]),
                    "end": int(parts[pos["end"]]),
                    "summit": int(parts[pos["summit"]]),
                    "mean_signal": float(parts[pos["mean_signal"]]),
                    "numsamples": int(parts[pos["numsamples"]]),
                    "component": parts[pos["component"]],
                }
            )
    return rows


def clean_200(seq: str) -> str | None:
    seq = seq.upper()
    if len(seq) != 200 or any(base not in "ACGT" for base in seq):
        return None
    return seq


def dinuc_shuffle(seq: str, rng: random.Random) -> str:
    pairs = [seq[i:i + 2] for i in range(0, len(seq), 2)]
    rng.shuffle(pairs)
    shuffled = "".join(pairs)
    if len(shuffled) == 200:
        return shuffled
    return shuffled[:200].ljust(200, "A")


def gc_random(length: int, gc: float, rng: random.Random) -> str:
    seq = []
    for _ in range(length):
        if rng.random() < gc:
            seq.append("G" if rng.random() < 0.5 else "C")
        else:
            seq.append("A" if rng.random() < 0.5 else "T")
    return "".join(seq)


def extract_by_chrom(rows: list[dict[str, object]], twobit: TwoBit) -> dict[int, str]:
    by_chrom: dict[str, list[tuple[int, dict[str, object]]]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_chrom[str(row["chrom"])].append((i, row))
    result = {}
    for chrom in sorted(by_chrom):
        chrom_seq = twobit.sequence(chrom)
        clen = len(chrom_seq)
        for i, row in by_chrom[chrom]:
            summit = int(row["summit"])
            start = summit - 100
            end = summit + 100
            if start < 0 or end > clen:
                continue
            seq = clean_200(chrom_seq[start:end])
            if seq is not None:
                result[i] = seq
    return result


def main() -> None:
    np_rng = np.random.default_rng(SEED)
    py_rng = random.Random(SEED)

    weights = load_mixture_weights()
    primary_n = 42_000
    # Draw extra rows so failed windows or Ns do not reduce the final count.
    selected = weighted_indices(weights, 55_000, np_rng)
    rows = read_selected_dhs(selected)

    twobit = TwoBit(TWOBIT_PATH)
    extracted = extract_by_chrom(rows, twobit)

    dhs_rows = [(rows[i], seq) for i, seq in extracted.items()]
    dhs_rows.sort(key=lambda x: (
        -float(x[0]["mean_signal"]),
        -int(x[0]["numsamples"]),
        str(x[0]["component"]),
    ))

    # Keep a strong invariant/high-confidence core and a broad topic-weighted
    # tail by shuffling after rank filtering.
    dhs_rows = dhs_rows[:50_000]
    py_rng.shuffle(dhs_rows)
    primary = [seq for _row, seq in dhs_rows[:primary_n]]
    control_source = [seq for _row, seq in dhs_rows[primary_n:primary_n + 8_000]]

    sequences = []
    seen = set()

    def add(seq: str) -> None:
        if len(sequences) >= N_TOTAL:
            return
        seq = clean_200(seq)
        if seq is not None and seq not in seen:
            seen.add(seq)
            sequences.append(seq)

    for seq in primary:
        add(seq)

    # Hard negatives: preserve dinucleotide-ish composition in active DHS
    # sequence while disrupting motif order.
    for seq in control_source[:3_000]:
        add(dinuc_shuffle(seq, py_rng))

    # Flanking genomic controls near DHSs but offset from the summit.
    flank_rows = []
    for row, _seq in dhs_rows[primary_n:primary_n + 6_000]:
        offset = py_rng.choice([-700, -500, 500, 700])
        copied = dict(row)
        copied["summit"] = int(copied["summit"]) + offset
        flank_rows.append(copied)
    flanks = extract_by_chrom(flank_rows, twobit)
    for i in sorted(flanks):
        add(flanks[i])

    # GC-stratified random controls, including promoter-like GC-rich sequence.
    gc_bins = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
    while len(sequences) < N_TOTAL:
        add(gc_random(200, py_rng.choice(gc_bins), py_rng))

    py_rng.shuffle(sequences)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(sequences) + "\n")
    print(f"wrote {OUT} with {len(sequences)} sequences")


if __name__ == "__main__":
    main()
