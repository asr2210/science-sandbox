# 029 — Exp 012 recipe with seed=2202 (3rd seed sample)

## Method
Identical recipe to exp 012; seed=2202.

## Results (eval_01)
mean_r = -0.0003 (K562=-0.0004, HepG2=+0.0004, SKNSH=-0.0009)

## Lesson — confirmed
- Seed-only variability: exp 012 (seed 501) +0.0045, exp 028 (2101) -0.0003,
  exp 029 (2202) -0.0003.
- exp 012's +0.0045 was a LUCKY OUTLIER. The recipe's typical eval_01
  is around -0.0003 ± noise.
- The "ceiling at +0.0045" was actually the max of ~15 noisy samples.
- True signal strength of any single recipe is small; observed effects
  are dominated by per-seed sample variance.

## Implication
- Need to test recipe robustness, not just compare top eval_01 scores.
- exp 005 (GC=50/50, +0.0043) also had only one seed tested — may be
  lucky too.
- For final exp 030, test exp 005 recipe with new seed to gauge whether
  it's a more robust recipe than exp 012.

## Next (exp 030)
Re-seed exp 005 (K562 motifs 8/seq, GC=50/50). If this lands ≥ +0.0030,
exp 005's design is more robust. If it lands near 0, both recipes are
noise-dominated and exp 012's score was pure luck.
