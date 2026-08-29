"""Experiment 029: narrow GC + 1 STOCHASTIC PWM motif at fixed center.

Like exp 021 but motif is sampled stochastically from PWM each time
(not consensus). Provides more natural motif variability.
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


def parse_meme_pwms(path: Path) -> list[np.ndarray]:
    text = path.read_text()
    blocks = re.split(r"\nMOTIF ", text)
    out = []
    for b in blocks[1:]:
        m = re.search(r"letter-probability matrix:.*", b)
        if not m:
            continue
        rest = b[m.end():]
        rows = []
        for line in rest.splitlines():
            line = line.strip()
            if not line or line.startswith("URL"):
                if rows:
                    break
                continue
            try:
                vals = [float(x) for x in line.split()]
            except ValueError:
                if rows:
                    break
                continue
            if len(vals) == 4:
                rows.append(vals)
        if rows:
            arr = np.array(rows)
            arr = arr / arr.sum(axis=1, keepdims=True)  # normalize
            out.append(arr)
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet_arr = np.array(list("ACGT"))
    pwms = [p for p in parse_meme_pwms(JASPAR) if 6 <= len(p) <= 20]
    print(f"loaded {len(pwms)} PWMs")

    gcs = np.clip(rng.normal(GC_MEAN, GC_STD, size=N_SEQS), 0.35, 0.65)
    pwm_choices = rng.integers(0, len(pwms), size=N_SEQS)
    seqs_arr = np.empty((N_SEQS, SEQ_LEN), dtype="<U1")

    for i in range(N_SEQS):
        gc = gcs[i]
        p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
        idx = rng.choice(4, size=SEQ_LEN, p=p)
        row = alphabet_arr[idx]
        # sample motif stochastically
        pwm = pwms[pwm_choices[i]]
        L = len(pwm)
        start = (SEQ_LEN - L) // 2
        motif_idx = np.array([rng.choice(4, p=pwm[j]) for j in range(L)])
        row[start:start + L] = alphabet_arr[motif_idx]
        seqs_arr[i] = row

    seqs = ["".join(row) for row in seqs_arr]
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
