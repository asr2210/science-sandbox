"""Experiment 014: combine 012 (fixed-center motif) + 013 (narrow target GC).

Background: per-seq target GC ~ Normal(0.5, 0.02).
Insertion: 1 JASPAR consensus motif at fixed center position.
Tests whether the two small gains stack.
"""
from pathlib import Path
import numpy as np
import re

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
JASPAR = REPO / "data" / "jaspar2024_vert.meme"


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
        consensus = "".join(alphabet[i] for i in idx)
        out.append(consensus)
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet_arr = np.array(list("ACGT"))

    motifs = parse_meme_consensus(JASPAR)
    motifs = [m for m in motifs if 6 <= len(m) <= 20]
    print(f"loaded {len(motifs)} motifs")

    # Per-seq GC targets
    gcs = np.clip(rng.normal(GC_MEAN, GC_STD, size=N_SEQS), 0.35, 0.65)

    seqs_arr = np.empty((N_SEQS, SEQ_LEN), dtype="<U1")
    motif_choices = rng.integers(0, len(motifs), size=N_SEQS)

    for i in range(N_SEQS):
        gc = gcs[i]
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        row = alphabet_arr[idx]
        m = motifs[motif_choices[i]]
        L = len(m)
        start = (SEQ_LEN - L) // 2
        for j, c in enumerate(m):
            row[start + j] = c
        seqs_arr[i] = row

    seqs = ["".join(row) for row in seqs_arr]

    realized_gc = np.array(
        [(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]]
    )
    print(f"realized GC: mean={realized_gc.mean():.3f} std={realized_gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
