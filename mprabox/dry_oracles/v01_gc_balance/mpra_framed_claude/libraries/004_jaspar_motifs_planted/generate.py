"""004_jaspar_motifs_planted: 50k random backbones with 2-4 planted JASPAR motifs.

Tests: do TF binding motifs alone (in random context) capture enough
regulatory signal to compete with real cCREs? If yes, motifs are sufficient
and synthetic libraries could replace cCREs. If much weaker, context matters.

Generalization rationale: motifs from 879 vertebrate JASPAR TFs span the
universe of TF binding specificities. A model trained on motif-rich random
backbones learns motif → activity for every TF family, which should transfer
to unseen cell types whose dominant TFs differ from K562/HepG2/SK-N-SH.

Design:
- 200bp uniform random backbone
- K ~ Uniform{2,3,4} motifs planted per sequence
- Each motif: pick a random JASPAR PWM, sample a sequence from it, plant at
  a random non-overlapping position
"""
import os
import re

import numpy as np

ROOT = "/data/users/arao/.private/MPRAgent_adversarial/runs/v01/blind_claude"
JASPAR_PATH = f"{ROOT}/data/jaspar/JASPAR2024_CORE_vertebrates_non-redundant_pfms_jaspar.txt"
OUT_PATH = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

L = 200
N = 50000
RNG_SEED = 4
ALPHABET = np.array(list("ACGT"))


def parse_jaspar(path):
    """Returns list of (name, ppm) where ppm is (L, 4) probability matrix."""
    motifs = []
    name = None
    rows = {}
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if line.startswith(">"):
                if name is not None and len(rows) == 4:
                    ppm = _rows_to_ppm(rows)
                    if ppm is not None:
                        motifs.append((name, ppm))
                name = line[1:]
                rows = {}
            else:
                m = re.match(r"^([ACGT])\s*\[(.*?)\]", line)
                if m:
                    base = m.group(1)
                    vals = [float(x) for x in m.group(2).split()]
                    rows[base] = vals
        if name is not None and len(rows) == 4:
            ppm = _rows_to_ppm(rows)
            if ppm is not None:
                motifs.append((name, ppm))
    return motifs


def _rows_to_ppm(rows):
    A = rows["A"]; C = rows["C"]; G = rows["G"]; T = rows["T"]
    if not (len(A) == len(C) == len(G) == len(T)):
        return None
    counts = np.array([A, C, G, T], dtype=np.float64).T  # (L, 4)
    counts += 0.25  # pseudocount
    ppm = counts / counts.sum(axis=1, keepdims=True)
    return ppm


def sample_from_ppm(ppm, rng):
    """Sample a sequence (string) from a PPM by independent column sampling."""
    L_m = ppm.shape[0]
    chars = []
    for i in range(L_m):
        b = rng.choice(4, p=ppm[i])
        chars.append("ACGT"[b])
    return "".join(chars)


def plant_motifs(backbone_arr, motifs, rng, k_choices=(2, 3, 4)):
    """Plant K motifs at non-overlapping positions. backbone_arr: np.array of L chars."""
    K = rng.choice(k_choices)
    occupied = []
    for _ in range(K):
        mi = rng.integers(0, len(motifs))
        _, ppm = motifs[mi]
        mseq = sample_from_ppm(ppm, rng)
        ml = len(mseq)
        if ml > L:
            continue
        # Find a free spot (up to 20 tries)
        for _ in range(20):
            pos = rng.integers(0, L - ml + 1)
            if all(not (pos < oe and pos + ml > os_) for (os_, oe) in occupied):
                backbone_arr[pos:pos + ml] = list(mseq)
                occupied.append((pos, pos + ml))
                break
    return backbone_arr


def main():
    print("Parsing JASPAR PWMs...", flush=True)
    motifs = parse_jaspar(JASPAR_PATH)
    print(f"  loaded {len(motifs)} motifs", flush=True)

    rng = np.random.default_rng(RNG_SEED)

    # Pre-generate random backbones
    print("Generating backbones...", flush=True)
    bb_idx = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    bb = ALPHABET[bb_idx]  # (N, L) np.str_

    print("Planting motifs...", flush=True)
    seqs = []
    for n in range(N):
        row = list(bb[n].tolist())  # list of single chars
        row = plant_motifs(row, motifs, rng)
        seqs.append("".join(row))
        if (n + 1) % 10000 == 0:
            print(f"  {n+1}/{N}", flush=True)

    with open(OUT_PATH, "w") as f:
        for s in seqs:
            assert len(s) == L
            f.write(s); f.write("\n")
    print(f"Wrote {len(seqs)} sequences", flush=True)


if __name__ == "__main__":
    main()
