"""Experiment 012: random uniform + ONE consensus motif at fixed center position.

Most MPRAs use a STAR sequence where a motif is inserted at a fixed position
in random flanks. Tests whether putting the motif at a deterministic LOCATION
(rather than random Poisson-sampled positions like exp 005/006) makes it
visible to the model. Motif sampled uniformly across the 879 vertebrate JASPAR
motifs, consensus form (no PWM stochastic sampling — pure dominant base).
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


def parse_meme_consensus(path: Path) -> list[str]:
    """Return list of consensus strings (one per motif), using argmax of each
    position in the PWM. Pure ACGT."""
    text = path.read_text()
    blocks = re.findall(
        r"letter-probability matrix:.*?(?:\n\n|\nMOTIF |\Z)", text, re.DOTALL
    )
    out = []
    alphabet = "ACGT"
    for b in blocks:
        # first line is the header; rest are 4-column rows
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
        arr = np.array(rows)  # (L, 4)
        idx = arr.argmax(axis=1)
        consensus = "".join(alphabet[i] for i in idx)
        out.append(consensus)
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))

    motifs = parse_meme_consensus(JASPAR)
    motifs = [m for m in motifs if 6 <= len(m) <= 20]
    print(f"loaded {len(motifs)} usable motifs")

    motif_choices = rng.integers(0, len(motifs), size=N_SEQS)

    # Random uniform background
    bg_idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    seqs_arr = alphabet[bg_idx]  # (N, 200)

    # Insert each motif at center
    for i in range(N_SEQS):
        m = motifs[motif_choices[i]]
        L = len(m)
        start = (SEQ_LEN - L) // 2
        for j, c in enumerate(m):
            seqs_arr[i, start + j] = c

    seqs = ["".join(row) for row in seqs_arr]

    assert all(len(s) == SEQ_LEN for s in seqs)
    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
