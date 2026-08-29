"""Experiment 028: narrow GC + fixed 5'/3' primer-like frame.

Add a fixed 10bp "primer" at start (CTAGCATGCG) and end (AGCTCAGTGC) of every
sequence. Tests if rigid structural framing (like MPRA constructs) helps.
Inner 180bp is narrow-GC random.
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
PRIMER_LEN = 10
SEED = 0
GC_MEAN = 0.50
GC_STD = 0.02
HERE = Path(__file__).resolve()

PRIMER_5 = "CTAGCATGCG"
PRIMER_3 = "AGCTCAGTGC"
assert len(PRIMER_5) == PRIMER_LEN
assert len(PRIMER_3) == PRIMER_LEN

INNER_LEN = SEQ_LEN - 2 * PRIMER_LEN  # 180


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))
    seqs = []
    for _ in range(N_SEQS):
        gc = float(np.clip(rng.normal(GC_MEAN, GC_STD), 0.35, 0.65))
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=INNER_LEN, p=p)
        inner = "".join(alphabet[idx])
        seqs.append(PRIMER_5 + inner + PRIMER_3)
    realized = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"realized GC: mean={realized.mean():.3f} std={realized.std():.3f}")
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
