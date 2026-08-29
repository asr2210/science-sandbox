"""Experiment 015 — 90/10 pELS + dELS.

45K pELS + 5K dELS. Tests "small mixing" hypothesis. Exp 013
showed 50/50 dilutes -0.025; this asks if 10% dELS spike still
dilutes (no-mix iron-clad) or specifically lifts dELS-favoring
evals (07, 13) without hurting pELS-driven gains.
"""
from __future__ import annotations

import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXP002_DIR = os.path.join(ROOT, "libraries", "002_encode_ccre")
sys.path.insert(0, EXP002_DIR)
from generate import (  # type: ignore  # noqa: E402
    extract_window,
    GENOME_2BIT,
    SEQ_LEN,
    ALPHABET,
    CCRE_BED,
)
from twobitreader import TwoBitFile

N_PELS = 45_000
N_DELS = 5_000
N_SEQS = N_PELS + N_DELS
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_classes(targets: tuple[str, ...]) -> dict[str, list[tuple[str, int, int]]]:
    out: dict[str, list[tuple[str, int, int]]] = {t: [] for t in targets}
    with open(CCRE_BED) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[-1] in out:
                out[parts[-1]].append((parts[0], int(parts[1]), int(parts[2])))
    return out


def sample_class(rng: np.random.Generator, pool: list, n: int, genome: TwoBitFile) -> list[str]:
    out: list[str] = []
    idx = rng.permutation(len(pool))
    i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = np.concatenate([idx, rng.permutation(len(pool))])
        chrom, start, end = pool[int(idx[i])]
        i += 1
        seq = extract_window(genome, chrom, start, end)
        if seq is None:
            continue
        out.append(seq)
    return out


def generate(seed: int, by_class: dict[str, list], genome: TwoBitFile) -> list[str]:
    rng = np.random.default_rng(seed)
    out = sample_class(rng, by_class["pELS"], N_PELS, genome)
    out.extend(sample_class(rng, by_class["dELS"], N_DELS, genome))
    rng.shuffle(out)
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading pELS, dELS cCREs...")
    by_class = load_classes(("pELS", "dELS"))
    print(f"  pELS: {len(by_class['pELS'])}, dELS: {len(by_class['dELS'])}")
    print("opening hg38.2bit...")
    genome = TwoBitFile(GENOME_2BIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}: 45K pELS + 5K dELS...")
        seqs = generate(seed, by_class, genome)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
