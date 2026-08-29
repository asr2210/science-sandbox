"""Experiment 022 — chr22 NON-REPEAT (uppercase) random tiles.

CRITICAL INSIGHT from exp 021 (Markov mimic):
- SKNSH score WENT UP by 0.036 (0.617 -> 0.654) for synthetic dinuc-mimic
- HepG2 CRASHED -0.32 (real DNA has structure HepG2 needs)

chr22 is 41% soft-masked (lowercase = repeats: Alu, LINE, etc).
If we filter to windows that are >80% UPPERCASE (mostly non-repeat
real DNA), we keep HepG2-friendly structure while removing repeats
that may hurt SKNSH.

Hypothesis: this beats chr22 random (0.3202).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(22)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip())  # preserve case
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

out = Path(__file__).parent / "sequences_0.txt"
ok = 0; tries = 0; rejected_repeat = 0
gcs = []
with out.open("w") as f:
    while ok < N:
        tries += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s.upper(): continue
        # filter: at least 80% uppercase (non-repeat)
        upper = sum(1 for c in s if c.isupper())
        if upper < int(0.80 * L):
            rejected_repeat += 1
            continue
        s_up = s.upper()
        if any(s_up.count(c * 20) > 0 for c in "ACGT"): continue
        f.write(s_up); f.write("\n")
        ok += 1
        if ok <= 5000:
            gcs.append((s_up.count("G") + s_up.count("C")) / L)
print(f"Wrote {ok} (tries {tries}, repeat-rejected {rejected_repeat}, accept {ok/tries:.2f})")
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
