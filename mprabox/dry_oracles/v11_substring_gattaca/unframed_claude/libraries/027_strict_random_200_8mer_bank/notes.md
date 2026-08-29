# 027 — 200-bank 8-mer insert (push K562 trend)

## Hypothesis
Per-cell K562 grew with bank size: 3→9→50 gave 0.852→0.855→0.862.
Maybe 200-bank pushes K562 above 0.862.

## Result
- eval_01 mean=**0.8753** (K562 0.8480, HepG2 0.9048, SKNSH 0.8730)
- vs 017 (50-bank): mean -0.007. K562 -0.014. SKNSH +0.001.

## Interpretation
K562 trend REVERSED: 200-bank K562=0.848 < 50-bank K562=0.862.
Either bank-size saturated around 50, or this is seed noise (see 028).
HepG2 also dropped slightly.

## Lesson
50-bank is the K562 sweet spot. Going larger doesn't help.

## Next
028: variance check — rerun 017 recipe with a different seed.
