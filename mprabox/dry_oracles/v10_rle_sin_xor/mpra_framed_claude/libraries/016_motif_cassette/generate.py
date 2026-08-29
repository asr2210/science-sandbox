"""Experiment 016: motif cassette — 5 JASPAR consensus motifs at fixed positions.

Builds on exp 012's gain. Place 5 motifs at fixed positions (centered at
30, 70, 100, 130, 170) with random uniform background. Tests whether more
motif density per sequence helps the model see TF importance signal.
"""
from pathlib import Path
import numpy as np
import re

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
JASPAR = REPO / "data" / "jaspar2024_vert.meme"
CENTERS = [30, 70, 100, 130, 170]


def parse_meme_consensus(path: Path) -> list[str]:
    text = path.read_text()
    blocks = re.findall(
        r"letter-probability matrix:.*?(?:\n\n|\nMOTIF |\Z)", text, re.DOTALL
    )
    out = []
    alphabet = "ACGT"
    for b in blocks:
        rows = []
        for line in b.splitlines()[1:]:
            line = line.strip()
            if not line:
                continue
            try:
                vals = [float(x) for x in line.split()]
            except ValueError:
                break
            if len(vals) == 4:
                rows.append(vals)
        if not rows:
            continue
        arr = np.array(rows)
        idx = arr.argmax(axis=1)
        out.append("".join(alphabet[i] for i in idx))
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet_arr = np.array(list("ACGT"))

    motifs = parse_meme_consensus(JASPAR)
    motifs = [m for m in motifs if 6 <= len(m) <= 14]
    print(f"loaded {len(motifs)} motifs (length 6-14)")

    bg_idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    seqs_arr = alphabet_arr[bg_idx]

    n_motifs = len(CENTERS)
    motif_choices = rng.integers(0, len(motifs), size=(N_SEQS, n_motifs))

    for i in range(N_SEQS):
        for k, center in enumerate(CENTERS):
            m = motifs[motif_choices[i, k]]
            L = len(m)
            start = center - L // 2
            for j, c in enumerate(m):
                if 0 <= start + j < SEQ_LEN:
                    seqs_arr[i, start + j] = c

    seqs = ["".join(row) for row in seqs_arr]

    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
