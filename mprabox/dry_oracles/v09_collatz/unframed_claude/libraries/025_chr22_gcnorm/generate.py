"""Experiment 025 — chr22 random + gentle GC normalization (no filtering).

For each chr22 tile, if GC < 45% flip a few A/T -> G/C; if GC > 53% flip
some G/C -> A/T. Push extreme tiles GENTLY toward 47-50% (SKNSH sweet
spot) without throwing away any window or removing repeats.

Hypothesis: lifts SKNSH (more tiles near 50% GC) with minimal HepG2
displacement (since we modify <5% of bases in only the tail windows).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(25)
N, L = 50_000, 200
TARGET_LO, TARGET_HI = 0.45, 0.53
TARGET = 0.49

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

def gc_normalize(s, target=TARGET, lo=TARGET_LO, hi=TARGET_HI, rng=None):
    n = len(s)
    cur_gc = (s.count("G") + s.count("C")) / n
    if lo <= cur_gc <= hi:
        return s, 0
    s_list = list(s)
    if cur_gc < lo:
        # need to flip some A/T -> G/C
        target_gc_count = int(target * n)
        cur_gc_count = int(cur_gc * n)
        need = target_gc_count - cur_gc_count
        at_positions = [i for i, c in enumerate(s_list) if c in "AT"]
        rng.shuffle(at_positions)
        for i in at_positions[:need]:
            s_list[i] = "G" if rng.random() < 0.5 else "C"
        return "".join(s_list), need
    else:  # cur_gc > hi
        target_gc_count = int(target * n)
        cur_gc_count = int(cur_gc * n)
        need = cur_gc_count - target_gc_count
        gc_positions = [i for i, c in enumerate(s_list) if c in "GC"]
        rng.shuffle(gc_positions)
        for i in gc_positions[:need]:
            s_list[i] = "A" if rng.random() < 0.5 else "T"
        return "".join(s_list), need

out = Path(__file__).parent / "sequences_0.txt"
ok = 0
flips = []
with out.open("w") as f:
    while ok < N:
        pos = int(rng.integers(0, len(seq) - L))
        s = seq[pos:pos + L]
        if "N" in s: continue
        if any(s.count(c * 20) > 0 for c in "ACGT"): continue
        s2, n_flips = gc_normalize(s, rng=rng)
        f.write(s2); f.write("\n")
        ok += 1
        if ok <= 5000:
            flips.append(n_flips)
print(f"Wrote {ok}; mean flips/seq={np.mean(flips):.2f}, median={np.median(flips):.0f}, max={max(flips)}")
print(f"Fraction with flips: {sum(1 for x in flips if x>0)/len(flips):.3f}")
