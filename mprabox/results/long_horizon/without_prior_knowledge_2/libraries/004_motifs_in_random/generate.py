"""Experiment 004: real TF motifs embedded in uniform random scaffolds.

50K x 200bp uniform random scaffolds. Per sequence, embed 1-3 motif
instances sampled from JASPAR 2024 CORE vertebrate non-redundant PWMs
(2,346 motifs). Each slot: pick motif uniformly at random, sample a
concrete sequence from the PWM, place at random non-overlapping
position.

Tests T3: motif content + broad coverage should beat both 001 (random,
no motifs) and possibly 002 (cCREs, motifs but narrower coverage).
"""
import os
import re
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
JASPAR = os.path.join(ROOT, "data", "motifs", "JASPAR2024_CORE_vertebrates_nr.jaspar")

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = np.array(list("ACGT"))
BASES = "ACGT"
MIN_MOTIFS = 1
MAX_MOTIFS = 3


def parse_jaspar(path):
    motifs = []
    cur_id, rows = None, {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if cur_id is not None and len(rows) == 4:
                    motifs.append((cur_id, rows))
                cur_id = line[1:].split("\t", 1)[0]
                rows = {}
            else:
                m = re.match(r"^([ACGT])\s*\[(.*)\]\s*$", line)
                if m:
                    rows[m.group(1)] = np.array(
                        [int(x) for x in m.group(2).split()], dtype=float
                    )
        if cur_id is not None and len(rows) == 4:
            motifs.append((cur_id, rows))
    # Convert each PWM to per-position probabilities (length L x 4)
    norm_motifs = []
    for mid, r in motifs:
        L = len(r["A"])
        mat = np.stack([r[b] for b in BASES], axis=1)  # (L,4)
        mat = mat + 0.01  # pseudocount
        mat = mat / mat.sum(axis=1, keepdims=True)
        norm_motifs.append((mid, mat))
    return norm_motifs


def sample_instance(pwm_mat, rng):
    """pwm_mat: (L,4) probabilities. Returns L-base string."""
    L = pwm_mat.shape[0]
    cdf = np.cumsum(pwm_mat, axis=1)
    u = rng.random(L)
    idx = (cdf < u[:, None]).sum(axis=1)
    return "".join(BASES[i] for i in idx)


def random_scaffold(rng, length):
    return "".join(ALPHABET[rng.integers(0, 4, size=length)])


def embed_motifs(scaffold, motifs, rng):
    n_motifs = int(rng.integers(MIN_MOTIFS, MAX_MOTIFS + 1))
    seq = list(scaffold)
    occupied = []  # list of (start, end) ranges
    for _ in range(n_motifs):
        midx = int(rng.integers(0, len(motifs)))
        _, pwm = motifs[midx]
        L = pwm.shape[0]
        if L >= SEQ_LEN:
            continue
        # pick a random non-overlapping position, retry up to 20 times
        placed = False
        for _try in range(20):
            start = int(rng.integers(0, SEQ_LEN - L + 1))
            end = start + L
            if all(end <= s or start >= e for s, e in occupied):
                instance = sample_instance(pwm, rng)
                # randomly orient (50% reverse-complement) — TFs bind both strands
                if rng.random() < 0.5:
                    instance = revcomp(instance)
                for i, c in enumerate(instance):
                    seq[start + i] = c
                occupied.append((start, end))
                placed = True
                break
        # if can't place after 20 tries, skip
    return "".join(seq)


_RC = str.maketrans("ACGT", "TGCA")
def revcomp(s):
    return s.translate(_RC)[::-1]


def generate(seed, motifs):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(N_SEQS):
        scaf = random_scaffold(rng, SEQ_LEN)
        seq = embed_motifs(scaf, motifs, rng)
        out.append(seq)
    return out


def main():
    print(f"loading motifs from {JASPAR}")
    motifs = parse_jaspar(JASPAR)
    print(f"  {len(motifs)} PWMs")
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, motifs)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
