"""Experiment 024: narrow GC + center motif, seed=999 (3rd combo replicate).

021 (s=42) gave 0.5222 (new best); 014 (s=0) gave 0.5196.
Need third seed to bound combo variance.
"""
from pathlib import Path
import numpy as np
import re

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 999
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
JASPAR = REPO / "data" / "jaspar2024_vert.meme"


def parse_meme_consensus(path: Path) -> list[str]:
    text = path.read_text()
    blocks = re.findall(r"letter-probability matrix:.*?(?:\n\n|\nMOTIF |\Z)", text, re.DOTALL)
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
        if rows:
            arr = np.array(rows)
            out.append("".join(alphabet[i] for i in arr.argmax(axis=1)))
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet_arr = np.array(list("ACGT"))
    motifs = [m for m in parse_meme_consensus(JASPAR) if 6 <= len(m) <= 20]
    print(f"loaded {len(motifs)} motifs")

    gcs = np.clip(rng.normal(GC_MEAN, GC_STD, size=N_SEQS), 0.35, 0.65)
    motif_choices = rng.integers(0, len(motifs), size=N_SEQS)
    seqs_arr = np.empty((N_SEQS, SEQ_LEN), dtype="<U1")

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
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
