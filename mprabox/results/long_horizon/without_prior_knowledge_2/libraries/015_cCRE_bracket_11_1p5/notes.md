# 015 — cCRE bracket: 11K rare / 1.5K abundant

## Design
11K each rare (PLS, CA-CTCF, CA-TF, CA-H3K4me3) = 44K
1.5K each abundant (pELS, dELS, CA, TF) = 6K
Total 50K. Sits between 013 (10K/2.5K, 0.7900) and 014 (12.5K/0K, 0.7155).

## Results (mean over 3 seeds)
- eval_01 = **0.7391** (vs 013 0.7477 = **−0.009**)
- mean across 14 evals ≈ **0.7802** (vs 013 0.7900 = **−0.010**)

## Per-eval delta vs 013
01:−0.009 02:−0.009 03:−0.009 04:−0.008 05:−0.009 06:−0.009 07:−0.015
08:−0.015 09:−0.010 10:−0.007 11:−0.008 12:−0.008 13:−0.012 14:−0.009

**Loses on ALL 14 evals** by 0.007–0.015. Largest losses on
broad-coverage cluster (eval_07/08/13).

## Across-seed
eval_01: 0.7383 / 0.7320 / 0.7470 → SD ≈ 0.006. Very stable.

## Branching outcome
Pre-experiment branches:
- 015 > 013 → optimum closer to rare-only than 013 (no)
- 015 ≈ 013 → 1.5K abundant still enough (no, lost 0.010)
- 015 < 013 → 2.5K is the floor; 1.5K starts to collapse (yes)

Result: **015 < 013, modest collapse.** The abundant-class floor (T11)
manifests not as a sharp cliff between 2.5K → 0K (014's −0.075), but
as a graduated decline: 2.5K → 1.5K loses ~0.010, 1.5K → 0K loses
another ~0.065.

This pinpoints **013 (10K rare / 2.5K abundant) as the optimum** on
the inverse-frequency axis. Both increasing rare past 10K (with
matching abundant decrease) and decreasing abundant below 2.5K cost
performance.

Interesting symmetry: 015 mean = 0.7802 ≈ 012 mean = 0.7819 (within
SD). The two libraries differ — 015 has more rare (11K vs 8K) and
less abundant (1.5K vs 4.5K). The two changes roughly cancel,
confirming there's a continuous Pareto frontier between rare and
abundant counts on which 013 sits at the peak.

## What this updates in the theory
**T8 (now closed):** The inverse-frequency optimum for 8 ENCODE cCRE
classes at N=50K is **approximately 10K rare / 2.5K abundant** (rare
= PLS, CA-CTCF, CA-TF, CA-H3K4me3; abundant = pELS, dELS, CA, TF).
The function relating per-class count to library informativeness has
a maximum here; it falls off in both directions.

**T11 (refined):** The abundant-class floor is graduated. Going from
2.5K → 1.5K loses 0.010; from 1.5K → 0K loses 0.065. Effective floor
is around 2K-2.5K per abundant class.

## Best library so far
**013 cCRE extreme upweight (10K/2.5K), mean ≈ 0.7900**. CONFIRMED
near-optimum on the class-balance axis. Five experiments (006/012/
013/014/015) bracket it tightly.

## Most informative next experiment (016)
**Switch to a new axis: principled 1/sqrt(pool_size) per-class
weighting.** 013 used uniform-within-rare and uniform-within-abundant.
The 1/sqrt scheme says CA-TF (smallest pool, 26K) should get the most;
dELS (largest pool, 1.47M) the least. Counts:
PLS=9400, CA-CTCF=5700, CA-TF=12600, CA-H3K4me3=7300,
pELS=4100, dELS=1700, CA=4100, TF=6300 → 50K.

- 016 > 013 → 1/sqrt-pool is the right principle; further refinement
- 016 ≈ 013 → 013's coarse rare-vs-abundant split is sufficient
- 016 < 013 → dropping CA-CTCF to 5.7K hurts; "rare" classes are not
  uniformly information-dense (CA-CTCF info is high even with large pool)

This tests whether per-class info density really scales as 1/sqrt-pool
or whether some classes (e.g., CA-CTCF for its CTCF specificity) are
information-dense beyond what their pool size predicts.
