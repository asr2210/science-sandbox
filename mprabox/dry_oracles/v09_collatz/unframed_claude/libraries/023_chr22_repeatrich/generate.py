"""Experiment 023 — chr22 REPEAT-RICH windows (mostly lowercase).

Exp 022 showed K562 dropped when repeats removed. Test the inverse:
take chr22 windows that are >70% lowercase (repeat-rich). Does K562
spike? If yes, K562 model is calibrated to repetitive elements
(Alu/LINE), and we can fine-tune repeat content.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(23)
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
ok = 0; tries = 0
gcs = []
with out.open("w") as f:
    while ok < N:
        tries += 1
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s.upper(): continue
        lower = sum(1 for c in s if c.islower())
        if lower < int(0.70 * L):  # require >=70% lowercase
            continue
        s_up = s.upper()
        if any(s_up.count(c * 20) > 0 for c in "ACGT"): continue
        f.write(s_up); f.write("\n")
        ok += 1
        if ok <= 5000:
            gcs.append((s_up.count("G") + s_up.count("C")) / L)
print(f"Wrote {ok} (tries {tries}, accept {ok/tries:.3f})")
print(f"GC mean={np.mean(gcs):.3f} std={np.std(gcs):.3f}")
