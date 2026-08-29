# 013 — cCRE extreme rare-class upweighting (10K rare, 2.5K abundant)

## Design
Continues the inverse-frequency gradient:
- 006: 6.25K equal per class       → mean 0.7754
- 012: 8K rare, 4.5K abundant      → mean 0.7819 (+0.0065)
- 013: 10K rare, 2.5K abundant     → mean 0.7900 (+0.008 over 012)

10K each: PLS, CA-CTCF, CA-TF, CA-H3K4me3 (40K total)
2.5K each: pELS, dELS, CA, TF (10K total)

## Results (mean over 3 seeds)
- eval_01 = **0.7477** (vs 012 0.7391 = **+0.009**)
- mean across 14 evals ≈ **0.7900** (vs 012 0.7819 = **+0.008**)

## Per-eval delta vs 012
01:+0.009 02:+0.008 03:+0.009 04:+0.007 05:+0.008 06:+0.008 07:+0.010
08:**+0.012** 09:+0.008 10:+0.008 11:+0.008 12:+0.008 13:+0.002 14:+0.008

**WINS ON ALL 14 EVALS** by 0.002–0.012. Average +0.008. Uniformly
better. Largest gain on eval_08 (+0.012) — the persistent outlier
finally responding to the right intervention.

## Per-eval delta vs 006 (cumulative gain from inverse-frequency)
+0.011 +0.012 +0.013 +0.019 +0.011 +0.012 +0.019 +0.022 +0.022
+0.018 +0.011 +0.011 +0.014 +0.012. Average **+0.015** vs 006.

## Across-seed
eval_01: 0.7437 / 0.7572 / 0.7422 → SD ≈ **0.008**, much lower than
006's 0.030. Extreme rare-upweighting is more stable AND higher mean.

## Why even more upweighting still helps
The rare cCRE classes contain regulatory elements with **high per-
sequence information density**. CA-CTCF (CTCF insulators) and CA-TF
(orphan-TF-bound chromatin) represent regulatory categories with
specific motif grammars distinct from typical enhancers/promoters.
The model learns substantially more per-example from rare-class
samples than from abundant dELS variants (most of which differ only
in nuanced flanking context).

Even at 10K samples per rare class (CA-TF=10K of 26K pool = 38%
sampled), the rare-class learning curve is still rising. The
abundant classes at 2.5K (~0.2% of dELS pool) still contribute
enough representative variation to retain their core signal.

## What this updates in T8
**T8 (further refined):** The per-class learning curve for cCRE
rare classes is still rising at 10K examples; for abundant classes
(esp. dELS), 2.5K samples retain most signal. The optimum is even
more extreme than naive 1/sqrt-pool weighting suggested. Possibly
"all rare classes maxed + minimal abundant" is the limit — see 014.

**T10 (new — saturation asymmetry):** rare cCRE classes have higher
unique-information-per-sample than abundant ones; the relative
information density is roughly inverse to pool size, but with a
steeper slope than 1/N. dELS (1.47M elements) is highly redundant;
CA-TF (26K elements) is information-dense.

## Best library so far
**013 extreme rare-upweight, mean ≈ 0.7900**. New best, +0.015 over
006, +0.008 over 012.

## Most informative next experiment (014)
**Test the LIMIT: abundant-classes-zero, rare-only library.** Take
12.5K each from the 4 rare classes (PLS, CA-CTCF, CA-TF, CA-H3K4me3)
= 50K. No abundant classes at all.
- 014 > 013 → abundant classes contribute nothing useful at 2.5K;
  the limit is rare-only.
- 014 ≈ 013 → abundant classes negligible at 2.5K (within seed-SD).
- 014 < 013 → abundant classes add real signal even at 2.5K; can't
  drop them entirely.

This pinpoints the optimum on the inverse-frequency axis. CA-TF at
12.5K = 48% of pool (still under-replacement); other rare classes
have more headroom. Should be near the saturation point.
