"""Generate 50,000 uniform random 200bp sequences for three seeds.

Experiment 001 — baseline floor. Each base is sampled i.i.d. uniform from
{A, C, G, T}. No biology, no GC bias, no structure. Establishes the
performance floor against which structured libraries are measured.
"""
from __future__ import annotations

import os
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = np.array(list("ACGT"))
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate(seed: int) -> list[str]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    chars = ALPHABET[idx]
    return ["".join(row) for row in chars]


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= {"A", "C", "G", "T"} for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    for seed in (0, 1, 2):
        seqs = generate(seed)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"wrote {out}: {len(seqs)} seqs")
