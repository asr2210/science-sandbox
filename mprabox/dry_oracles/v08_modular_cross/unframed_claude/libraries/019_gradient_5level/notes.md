# 019 — 5-level gradient of motif density

## Method
5 levels x 10k: 0, 3, 6, 10, 18 motifs/seq (K562+universal panel), GC=50%.

## Results (eval_01)
mean_r = -0.0024 (K562=-0.0057, HepG2=+0.0012, SKNSH=-0.0028)

## Lesson
- eval_01 PREFERS BIMODAL over gradient — strict 50/50 active/null
  outperforms continuous density.
- BUT eval_08 went WILD HIGH: mean=+0.0084, K562=+0.0190, SKNSH=+0.0069
  (new record for eval_08). Different eval, different design preference.
- Gradient design fails primary metric.

## Implication
- For eval_01: must use 50/50 bimodal. Gradient is wrong shape.
- For eval_08: gradient density is the trick.

## Next (exp 020)
Back to bimodal. Try UNIVERSAL-ONLY motif saturation (no cell-specific
mixing) at GC=60 active vs GC=30 null. Hypothesis: universals activate
all 3 cells uniformly → all three r columns lift on eval_01 (vs exp 012
where HepG2 stayed flat).
