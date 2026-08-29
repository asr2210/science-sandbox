# 001 — cCRE class-balanced sampling

## Result
| metric  | this exp | dhs_topic (best baseline) | Δ |
|---------|----------|---------------------------|------|
| eval_01 | **0.7262** | 0.7232 | +0.0030 |
| eval_02 | 0.8190 | 0.8138 | +0.0052 |
| eval_03 | 0.8005 | 0.7933 | +0.0072 |
| eval_04 | 0.7935 | 0.7904 | +0.0031 |
| eval_05 | 0.7259 | 0.7230 | +0.0029 |
| eval_06 | 0.8191 | 0.8136 | +0.0055 |
| eval_07 | 0.7467 | 0.7398 | +0.0069 |
| eval_08 | 0.6849 | 0.7011 | **−0.0162** |
| eval_09 | 0.8634 | 0.8601 | +0.0033 |
| eval_10 | 0.7818 | 0.7904 | **−0.0086** |
| eval_11 | 0.7132 | 0.7098 | +0.0034 |
| eval_12 | 0.6890 | 0.6822 | +0.0068 |
| eval_13 | 0.7360 | 0.7271 | +0.0089 |
| eval_14 | 0.8194 | 0.8144 | +0.0050 |

Mean across 14 evals: **0.7656** (dhs_topic ≈ 0.7644). Wins on 12/14, loses on
two. Wall: 1237 s.

## Per-seed eval_01 (mean_r)
- seed 0: 0.6898
- seed 1: 0.7541
- seed 2: 0.7347

Spread = 0.064 across seeds — much larger than the +0.003 margin over dhs_topic.
The headline result is real but seed-noisy at n=3 (baselines averaged n=5).

## What I learned
1. **Annotation diversity at the class level is at least as valuable as NMF-
   topic-weighted DHS sampling.** A simple equal-counts mix of {PLS, pELS,
   dELS, CTCF-only, DNase-H3K4me3} matches or marginally beats the best
   prior baseline on most eval sets without any weighting machinery. This
   updates the working theory toward "category coverage" as a sufficient lever.
2. **CTCF-only and DNase-H3K4me3 are tiny pools (~26–36K) but not bottlenecks.**
   They contributed 10K each (~28%–39% of pool). High class membership of
   these structurally-important elements may explain the eval_07/eval_13 gains
   (+0.007 / +0.009) where the baselines that under-sample these classes lag.
3. **Loss on eval_08 (−0.016) is the only big negative.** eval_08 is the eval
   set where `synth_oracle` (random sequences) does surprisingly well in the
   baseline table (0.7696, the best of any strategy). This is a hint that
   eval_08 rewards sequence-level diversity beyond what genomic regulatory
   regions provide. Class-balancing made the library *less diverse* in
   sequence space (drops the abundant dELS class from 75% to 20%), which
   may have hurt eval_08.
4. **Per-seed variance is high.** Seed 0 was a 0.69 outlier; seeds 1+2 were
   0.73–0.75. Worth investigating whether the seed-0 sample happened to hit
   a degenerate region of the cCRE pool.

## What this implies for next experiments
- Test whether adding back a fraction of i.i.d. random sequences recovers
  eval_08 without losing the gains elsewhere (echoes Yin 2024's "mixed source
  beats single source").
- Test whether keeping the class balance but adding a non-accessible
  conserved-region class (where pioneer-factor motifs may live) helps
  generalization further.
- Investigate the seed-0 underperformance (is it a per-seed artifact, or a
  systematic property of how my sampling interacts with chromosome-level
  structure?).
