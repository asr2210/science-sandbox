"""Experiment 006: random uniform + heavy CONSENSUS JASPAR motif insertions.

Tests whether the null result in 005 was due to weak (stochastic) motif realizations
or because motifs are irrelevant to this benchmark. Now: K~Poisson(6) clamped
[3,10] motifs per sequence, each realized as the PWM consensus (argmax).
"""
from pathlib import Path
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0
LAMBDA = 6.0
MIN_MOTIFS = 3
MAX_MOTIFS = 10
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
            while i < len(lines) and not lines[i].startswith("letter-probability"):
                i += 1
            header = lines[i].split()
            w = int(header[header.index("w=") + 1])
            i += 1
            pwm = []
            for _ in range(w):
                pwm.append([float(x) for x in lines[i].split()])
                i += 1
            motifs.append(np.array(pwm, dtype=np.float64))
        else:
            i += 1
    return motifs


def consensus(pwm: np.ndarray) -> str:
    bases = np.array(["A", "C", "G", "T"])
    return "".join(bases[np.argmax(pwm, axis=1)])


def main() -> None:
    rng = np.random.default_rng(SEED)
    motifs = parse_meme(MEME_PATH)
    consensus_seqs = [consensus(m) for m in motifs]
    widths = np.array([m.shape[0] for m in motifs])
    print(f"parsed {len(motifs)} motifs; widths min={widths.min()} max={widths.max()} mean={widths.mean():.1f}")

    alphabet = np.array(["A", "C", "G", "T"])
    base_idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    base_chars = alphabet[base_idx]

    n_motifs_per = np.clip(rng.poisson(LAMBDA, size=N_SEQS), MIN_MOTIFS, MAX_MOTIFS)

    seqs: list[str] = []
    total_motifs = 0
    total_motif_bases = 0
    for s_idx in range(N_SEQS):
        seq = list(base_chars[s_idx])
        K = int(n_motifs_per[s_idx])
        placed: list[tuple[int, int]] = []
        for _ in range(K):
            attempts = 0
            while attempts < 50:
                attempts += 1
                m_idx = int(rng.integers(0, len(motifs)))
                w = widths[m_idx]
                if w >= SEQ_LEN:
                    continue
                start = int(rng.integers(0, SEQ_LEN - w + 1))
                end = start + w
                if any(not (end <= a or start >= b) for a, b in placed):
                    continue
                seq[start:end] = list(consensus_seqs[m_idx])
                placed.append((start, end))
                total_motifs += 1
                total_motif_bases += w
                break
        seqs.append("".join(seq))

    print(f"placed {total_motifs} motifs total ({total_motif_bases} bp)")
    print(f"avg motifs/seq = {total_motifs / N_SEQS:.2f}")
    print(f"avg motif bp/seq = {total_motif_bases / N_SEQS:.1f} of {SEQ_LEN}")
    gc = np.array([(s.count("G") + s.count("C")) / SEQ_LEN for s in seqs[:1000]])
    print(f"first-1000 GC: mean={gc.mean():.3f} std={gc.std():.3f}")

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:200])

    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
