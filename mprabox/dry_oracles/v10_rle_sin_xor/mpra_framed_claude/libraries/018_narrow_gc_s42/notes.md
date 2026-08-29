# 018 — replicate 013 (narrow target GC) with seed=42

## Design
Identical to 013 but SEED=42. Per-seq target GC ~ Normal(0.5, 0.02), then sample.

## Result
- eval_01 mean_r = **0.5210** (vs 013 seed=0: 0.5206)
- K562 r = 0.9946
- HepG2 r = 0.5665
- SK-N-SH r = 0.002

## Reading
**The narrow-GC gain is reproducible.** Both seeds give ~0.521. Random uniform baseline is 0.517-0.518. Gain ~0.003 is small but real (much larger than seed-to-seed variance of ~0.0005 within these designs).

Compare:
- Random uniform binomial (001 s0): 0.5177
- Random uniform binomial (010 s42): 0.5183
- Narrow target GC=N(0.5, 0.02) (013 s0): 0.5206
- Narrow target GC=N(0.5, 0.02) (018 s42): 0.5210

→ Per-seq GC mixture wins by ~0.003.

## Implication
Sweep GC std to find optimum. Try 0.04 (next exp), maybe 0.06. Map the curve.
