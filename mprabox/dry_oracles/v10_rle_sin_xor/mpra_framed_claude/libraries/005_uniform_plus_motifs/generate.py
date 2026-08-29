"""Experiment 005: random uniform 200bp with K~Poisson(2) JASPAR motif insertions.

Hypothesis: composition is at its ceiling with random uniform. Add motif content
by inserting real TF motif realizations into otherwise-random sequences. Should
preserve K562 (composition unchanged) while introducing motif features the model
can learn for HepG2 and (hopefully) SK-N-SH.

Motif source: JASPAR 2024 CORE vertebrates non-redundant (879 PWMs).
Per-sequence motif count: Poisson(lambda=2), capped at [1, 5].
Per-motif realization: stochastic sample from the PWM (PWM-weighted random base).
Insertion positions chosen at random; overlaps avoided.
"""
from pathlib import Path
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
LAMBDA = 2.0
MIN_MOTIFS = 1
MAX_MOTIFS = 5
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
MEME_PATH = REPO / "data" / "jaspar2024_vert.meme"


def parse_meme(path: Path):
    motifs = []
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("MOTIF "):
            parts = line.split()
            mid = parts[1]
            # find the letter-probability matrix line
            while i < len(lines) and not lines[i].startswith("letter-probability"):
                i += 1
            header = lines[i].split()
            w_idx = header.index("w=") + 1
            w = int(header[w_idx])
            i += 1
            pwm = []
            for _ in range(w):
                pwm.append([float(x) for x in lines[i].split()])
                i += 1
            motifs.append((mid, np.array(pwm, dtype=np.float64)))
        else:
            i += 1
    return motifs


def sample_realization(pwm: np.ndarray, rng: np.random.Generator) -> str:
    bases = np.array(["A", "C", "G", "T"])
    out = []
    for row in pwm:
        out.append(rng.choice(bases, p=row / row.sum()))
    return "".join(out)


def main() -> None:
    rng = np.random.default_rng(SEED)
    motifs = parse_meme(MEME_PATH)
    print(f"parsed {len(motifs)} motifs from {MEME_PATH.name}")
    widths = [m[1].shape[0] for m in motifs]
    print(f"motif widths: min={min(widths)} max={max(widths)} mean={np.mean(widths):.1f}")

    alphabet = np.array(["A", "C", "G", "T"])
    # Sample base sequences
    base_idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    base_chars = alphabet[base_idx]

    # For each sequence, decide how many motifs and place them
    n_motifs_per = np.clip(rng.poisson(LAMBDA, size=N_SEQS), MIN_MOTIFS, MAX_MOTIFS)

    seqs: list[str] = []
    total_motifs = 0
    total_motif_bases = 0
    for s_idx in range(N_SEQS):
        seq = list(base_chars[s_idx])
        K = int(n_motifs_per[s_idx])
        # Try to place K motifs without overlapping
        placed_intervals: list[tuple[int, int]] = []
        attempts = 0
        for _ in range(K):
            while attempts < 50:
                attempts += 1
                m_idx = int(rng.integers(0, len(motifs)))
                _, pwm = motifs[m_idx]
                w = pwm.shape[0]
                if w >= SEQ_LEN:
                    continue
                start = int(rng.integers(0, SEQ_LEN - w + 1))
                end = start + w
                # check no overlap
                if any(not (end <= a or start >= b) for a, b in placed_intervals):
                    continue
                # place
                inst = sample_realization(pwm, rng)
                seq[start:end] = list(inst)
                placed_intervals.append((start, end))
                total_motifs += 1
                total_motif_bases += w
                break
        seqs.append("".join(seq))

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    print(f"placed {total_motifs} motif instances total, {total_motif_bases} motif-bases")
    print(f"avg motifs/seq = {total_motifs / N_SEQS:.2f}")
    print(f"avg motif coverage per seq = {total_motif_bases / N_SEQS:.1f} bp of 200")
    # composition check
    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"first-1000 GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
