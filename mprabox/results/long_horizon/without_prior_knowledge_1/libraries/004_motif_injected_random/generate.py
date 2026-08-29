"""Experiment 004 — motif-injected random backgrounds.

Tests the hypothesis from exp 003 that the cCRE gain is motif-driven.
Each sequence: 200-bp uniform-random background with 1-5 TF binding-site
instances (sampled from JASPAR 2024 CORE non-redundant PWMs) inserted
at random non-overlapping positions on random strands.

Design choices:
- Number of motifs per sequence: uniform on {1,2,3,4,5}
- Motif identity: uniform sample from the 2,346-motif JASPAR pool
- Strand: 50/50 forward / reverse-complement
- Position: uniform random, non-overlapping with already-placed motifs
- Background outside motif instances: uniform random ACGT

This isolates "motifs alone" from "motifs in genomic context": the
backgrounds are uniform-composition (so we keep the regularization
benefit of wide composition coverage that exp 003 revealed) while
the motif content provides the regulatory grammar that exp 003 showed
is what generalizes.
"""
from __future__ import annotations

import os
import re
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = ("A", "C", "G", "T")
ALPHABET_SET = set(ALPHABET)
COMP = str.maketrans("ACGT", "TGCA")
PFM_PATH = os.path.join(ROOT, "data", "jaspar", "JASPAR2024_CORE_non-redundant_pfms_jaspar.txt")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_pfms(path: str) -> list[np.ndarray]:
    """Parse JASPAR PFMs. Returns list of (4, L) arrays of counts (rows ACGT)."""
    pfms = []
    with open(path) as f:
        block: dict[str, list[int]] = {}
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if block:
                    pfms.append(_block_to_arr(block))
                block = {}
                continue
            if not line:
                continue
            m = re.match(r"^([ACGT])\s*\[\s*([0-9.\s]+?)\s*\]\s*$", line)
            if not m:
                continue
            base = m.group(1)
            counts = [float(x) for x in m.group(2).split()]
            block[base] = counts
        if block:
            pfms.append(_block_to_arr(block))
    return pfms


def _block_to_arr(block: dict[str, list[float]]) -> np.ndarray:
    return np.array([block[b] for b in ALPHABET], dtype=np.float64)


def pfm_to_ppm(pfm: np.ndarray, pseudocount: float = 0.5) -> np.ndarray:
    """Convert PFM counts to position probability matrix with pseudocount."""
    p = pfm + pseudocount
    return p / p.sum(axis=0, keepdims=True)


def sample_instance(ppm: np.ndarray, rng: np.random.Generator) -> str:
    """Sample one DNA instance from a PPM (one base per column)."""
    L = ppm.shape[1]
    out = []
    for col in range(L):
        idx = rng.choice(4, p=ppm[:, col])
        out.append(ALPHABET[idx])
    return "".join(out)


def revcomp(s: str) -> str:
    return s.translate(COMP)[::-1]


def generate(seed: int, ppms: list[np.ndarray]) -> list[str]:
    rng = np.random.default_rng(seed)
    n_motif_choices = np.array([1, 2, 3, 4, 5])
    out: list[str] = []
    for _ in range(N_SEQS):
        # background
        bg_idx = rng.integers(0, 4, size=SEQ_LEN, dtype=np.uint8)
        seq = list("".join(ALPHABET[i] for i in bg_idx))
        # number of motifs
        n_mot = int(rng.choice(n_motif_choices))
        # try to place each motif
        placed: list[tuple[int, int]] = []  # (start, end) intervals
        attempts = 0
        for _m in range(n_mot):
            ppm = ppms[int(rng.integers(0, len(ppms)))]
            inst = sample_instance(ppm, rng)
            if rng.random() < 0.5:
                inst = revcomp(inst)
            L = len(inst)
            if L >= SEQ_LEN:
                # extreme edge case (no JASPAR motif is >50bp); skip
                continue
            placed_ok = False
            for _try in range(20):
                attempts += 1
                start = int(rng.integers(0, SEQ_LEN - L + 1))
                end = start + L
                # check overlap with already-placed
                if any(not (end <= s or start >= e) for s, e in placed):
                    continue
                seq[start:end] = list(inst)
                placed.append((start, end))
                placed_ok = True
                break
            # if 20 tries fail, just give up on that motif (sequence is dense)
        out.append("".join(seq))
    return out


def write_seqs(seqs: list[str], path: str) -> None:
    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= ALPHABET_SET for s in seqs)
    with open(path, "w") as f:
        f.write("\n".join(seqs) + "\n")


if __name__ == "__main__":
    print("loading JASPAR PFMs...")
    pfms = load_pfms(PFM_PATH)
    print(f"  loaded {len(pfms)} PFMs (lengths {min(p.shape[1] for p in pfms)}-{max(p.shape[1] for p in pfms)})")
    ppms = [pfm_to_ppm(p) for p in pfms]
    for seed in (0, 1, 2):
        print(f"generating seed {seed}...")
        seqs = generate(seed, ppms)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        write_seqs(seqs, out)
        print(f"  wrote {out}: {len(seqs)} seqs")
