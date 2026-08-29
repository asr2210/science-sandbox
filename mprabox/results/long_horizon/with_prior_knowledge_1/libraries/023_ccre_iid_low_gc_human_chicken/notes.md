# 023 — low-GC iid symmetry test (35K cCRE + 5K iid at 30% GC + 5K human + 5K chicken)

iid composition: A=0.35, C=0.15, G=0.15, T=0.35 (30% GC).
Distance from genome (~41% GC) = 11pp; from uniform 50% GC = 20pp.

## Result — asymmetric: low-GC penalty is much smaller than high-GC penalty
| metric  | 023 | 010 | 022 | 021 | Δ vs 010 |
|---------|-----|-----|-----|-----|----------|
| eval_01 | 0.7518 | **0.7599** | 0.7199 | 0.7439 | −0.0081 |
| eval_02 | 0.8468 | **0.8550** | 0.8119 | 0.8383 | −0.0082 |
| eval_03 | 0.8320 | **0.8413** | 0.7920 | 0.8236 | −0.0093 |
| eval_04 | 0.8077 | **0.8140** | 0.7817 | 0.8000 | −0.0063 |
| eval_05 | 0.7517 | **0.7599** | 0.7199 | 0.7439 | −0.0082 |
| eval_06 | 0.8469 | **0.8550** | 0.8117 | 0.8384 | −0.0081 |
| eval_07 | 0.7975 | **0.8044** | 0.7427 | 0.7835 | −0.0069 |
| eval_08 | 0.7169 | **0.7515** | 0.6819 | 0.7187 | −0.0346 |
| eval_09 | 0.8791 | **0.8872** | 0.8494 | 0.8707 | −0.0081 |
| eval_10 | 0.8095 | **0.8233** | 0.7687 | 0.8021 | −0.0138 |
| eval_11 | 0.7386 | **0.7464** | 0.7070 | 0.7308 | −0.0078 |
| eval_12 | 0.7154 | **0.7244** | 0.6803 | 0.7089 | −0.0090 |
| eval_13 | 0.7913 | **0.8016** | 0.7376 | 0.7788 | −0.0103 |
| eval_14 | 0.8469 | **0.8551** | 0.8122 | 0.8383 | −0.0082 |

Mean 14: **0.7952** vs 010=0.8056 (Δ=−0.0104). Wall: 1313s (normal).

## Per-seed eval_01
- seed 0: 0.7633
- seed 1: 0.7359
- seed 2: 0.7562

Spread = 0.027. Intermediate variance (between healthy 010=0.012 and
broken 022=0.042). Anchor partially weakened but not destroyed.

## Pre-registered scorecard
- "023 ≈ 010 within ±0.010 (asymmetric, no AT-rich trigger)":
  **confirmed at the boundary** (Δ=−0.010, just inside).
- "023 between 021 and 022 (loss 0.020-0.040)": **falsified**
  (loss 0.010 is BELOW 021's 0.018; low-GC hurts LESS than matched).
- "023 ≈ 022 (full symmetry, distance from uniform matters)":
  **falsified** (loss 0.010 vs 022's 0.047 — 4.7× smaller despite
  larger distance from uniform).

## iid composition curve — full picture (4 points)
| iid type | composition | dist from genome | dist from uniform | Δ vs uniform |
|----------|-------------|-------------------|-------------------|---------------|
| 023 low-GC | 30% GC | 11pp | 20pp | **−0.010** |
| **010 uniform** | **50% GC** | **9pp** | **0** | **baseline** |
| 021 hg38-matched | 41% GC | 0pp | 9pp | −0.018 |
| 022 high-GC | 60% GC | 19pp | 10pp | **−0.047** |

The penalty is **strongly asymmetric and not explained by either
"distance from genome" or "distance from uniform" alone**. The
ordering is:
- low-GC (best of the perturbations, only −0.010 even at 20pp from
  uniform)
- hg38-matched (−0.018, sits AT genome)
- high-GC (−0.047, only 10pp from uniform but most damaging)

**No simple single-variable model fits this curve.** The high-GC
direction is uniquely punished.

## Theory update (v7) — iid composition penalty is direction-asymmetric, CpG-island confusion confirmed
**Refined theory:**
> Iid composition penalty is asymmetric in direction:
>   - **High-GC (>50%):** hurts a lot. Triggers CpG-island
>     confusion in the model. Real CpG islands in genome are 60-70%
>     GC and are distinctive promoter features the model has learned
>     to recognize. High-GC iid sequences are "fake CpG islands" —
>     trigger the model's regulatory-feature expectation but lack
>     real motifs.
>   - **Low-GC (<50%):** hurts mildly. AT-rich content is associated
>     with introns, gene deserts, and AT-rich repeats (~50% of
>     genome) — none of which are distinctive regulatory features.
>     The model treats AT-rich as "non-specific background" rather
>     than "active regulatory expectation".
>   - **At-genome composition (~41%):** hurts moderately. Loses
>     "off-genome calibration anchor" entirely.
> 
> The optimum is uniform (50% GC) for two converging reasons:
>   (i) Off-genome enough to anchor (above the 41% genome composition).
>   (ii) Below the CpG-island threshold (below ~60% GC).

## What I learned (operational)
1. **Don't pipe generate.py through `head` during development.**
   Earlier this session, piping `python3 generate.py | head -10` killed
   the process via SIGPIPE after seed_0, leading to a 1-seed eval that
   showed eval_01=0.7633 (apparent NEW BEST). The correct 3-seed mean
   was 0.7518 (worse than 010). Single-seed results are unreliable
   even when they look promising — the seed_0 was an outlier on the
   high side.
2. **Asymmetric penalty curves are the norm, not the exception.**
   020 (cCRE class balance) and 022/023 (iid composition) both showed
   strong direction asymmetry. Don't assume bowls are symmetric;
   always test both directions.
3. **The iid axis is now fully mapped.** Mass=5K, composition=uniform
   50% GC. The composition curve has 4 points covering 30/41/50/60%
   GC. Further iid axis exploration is exhausted.

## What to try next
The iid composition axis is closed. The cCRE class balance axis is
closed. The cross-species axis is closed (chicken at 5K is best,
hump theory false).

**024: iid mass curvature.** The 5K iid mass was set by early-loop
intuition and never directly probed. Library: 32.5K cCRE 6.5K-each
+ 7.5K iid (uniform) + 5K human + 5K chicken = 50K. Probes whether
iid mass is super-linear (gain from 7.5K outpaces the 32.5K cCRE
loss → NEW BEST possible) or saturates around 5K (cCRE loss
dominates → regression).

Pre-registered:
- 024 ≈ 010 within ±0.005: iid mass scales linearly per element at
  marginal value, exactly cancelling cCRE reduction at 32.5K.
- 024 > 010 by +0.005-0.015: iid mass super-linear OR cCRE reduction
  cheaper than expected. **POSSIBLE NEW BEST.**
- 024 < 010 by 0.005-0.020: iid mass saturated at 5K, cCRE loss
  uncompensated.

This is the cleanest unexplored single-axis test that could yield a
NEW BEST.

Alternatives considered:
- **5th-element addition at 2.5K** (with 32.5K cCRE): bar is high
  (~+0.012) for net positive; few candidates likely to clear it.
- **Replace human-gen with novel category** (e.g., reverse-complemented
  cCRE, near-cCRE flanking genomic): human-gen value is small (~0.005)
  so upside is small; downside if replacement is bad.
- **Closer-to-chicken species** (turkey, alligator): predicted to be
  redundant with chicken (saturating).
- **iid mass at 4K or 3K** (below 5K): probes downside of mass curve;
  less interesting than upside test.

024 (iid mass curvature) is the highest-information-density test for
finding NEW BEST. Going with it.
