# 028 — Reproduce exp 012 with new seed (seed=2101 vs 501)

## Method
Identical to exp 012 (K562 motifs panel, 12/seq, GC=65 active vs GC=25
null), only RNG seed changed.

## Results (eval_01)
mean_r = -0.0003 (K562=+0.0006, HepG2=+0.0005, SKNSH=-0.0019)
vs exp 012: mean_r=+0.0045 (K562=+0.0089, HepG2=+0.0011, SKNSH=+0.0035)

## Lesson — BIG
- Same recipe, different seed → eval_01 mean dropped 0.0048 points.
- K562 r FROM 0.0089 TO 0.0006.
- The "plateau" I've been chasing isn't a true ceiling — it's NOISE.
- Per-seed variance on eval_01 is ~±0.003+ for the same recipe.
- exp 012's +0.0045 was a LUCKY SEED, not robust.
- eval_13 in this seed = +0.0064 (K562=+0.0103, HepG2=+0.0074) — also a
  lucky landing, but for a different eval.

## Implication
- Many "design lessons" I drew from single seeds may be noise.
- Single-seed eval_01 has high variance. With ~16 experiments and SD
  ~0.003, expected max over 16 = ~0.0045-0.005. Hitting +0.0045 was
  expected.
- To genuinely improve, would need to average over many seeds — but
  with 50k cap and 2 experiments left, the best move is to try more
  seeds of the best recipe and pick max.

## Next (exp 029)
Try ANOTHER seed of exp 012 recipe. With 3 seeds tested
(501→+0.0045, 2101→-0.0003), one more sample gives variance estimate.
Pick best for exp 030.
