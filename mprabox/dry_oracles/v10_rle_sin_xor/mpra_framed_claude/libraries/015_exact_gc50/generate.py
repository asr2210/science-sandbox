"""Experiment 015: deterministic GC = exactly 0.5 (every seq has 100 G+C, 100 A+T).

Tests whether the binomial GC variance in random uniform (std ≈ 0.035) is
helpful or hurtful. If exact GC=0.5 beats binomial, then GC variance hurts.
If it loses, the model needs the GC distribution to be wide.
Random uniform A/T choice within the A+T positions, random uniform C/G choice
within the G+C positions.
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
HERE = Path(__file__).resolve()


def main() -> None:
    rng = np.random.default_rng(SEED)

    # For each seq: pick exactly 100 of 200 positions to be GC, rest AT.
    # Then within GC positions, pick G or C uniformly. Within AT, A or T uniformly.
    seqs = []
    for _ in range(N_SEQS):
        # Positions of GC
        perm = rng.permutation(SEQ_LEN)
        gc_positions = perm[:SEQ_LEN // 2]
        seq = np.empty(SEQ_LEN, dtype="<U1")
        # Fill AT positions
        seq[:] = rng.choice(np.array(["A", "T"]), size=SEQ_LEN)
        # Override GC positions
        seq[gc_positions] = rng.choice(np.array(["C", "G"]), size=SEQ_LEN // 2)
        seqs.append("".join(seq))

    realized_gc = np.array(
        [(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]]
    )
    print(f"realized GC: mean={realized_gc.mean():.4f} std={realized_gc.std():.4f}")
    # should be exactly 0.5 std 0.0

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
