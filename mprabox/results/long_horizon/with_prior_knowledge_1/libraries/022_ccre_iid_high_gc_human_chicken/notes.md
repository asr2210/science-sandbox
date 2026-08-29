# 022 — extreme high-GC iid (35K cCRE + 5K iid at 60% GC + 5K human + 5K chicken)

iid composition: A=0.20, C=0.30, G=0.30, T=0.20 (60% GC).
Distance from genome (hg38 ~41% GC) = 19pp; vs uniform's 9pp.

## Result — extreme composition is much worse than uniform. Composition effect is non-monotonic
| metric  | 022 | 010 | 021 | Δ vs 010 | Δ vs 021 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7199 | **0.7599** | 0.7439 | −0.0400 | −0.0240 |
| eval_02 | 0.8119 | **0.8550** | 0.8383 | −0.0431 | −0.0264 |
| eval_03 | 0.7920 | **0.8413** | 0.8236 | −0.0493 | −0.0316 |
| eval_04 | 0.7817 | **0.8140** | 0.8000 | −0.0323 | −0.0183 |
| eval_05 | 0.7199 | **0.7599** | 0.7439 | −0.0400 | −0.0240 |
| eval_06 | 0.8117 | **0.8550** | 0.8384 | −0.0433 | −0.0267 |
| eval_07 | 0.7427 | **0.8044** | 0.7835 | −0.0617 | −0.0408 |
| eval_08 | 0.6819 | **0.7515** | 0.7187 | −0.0696 | −0.0368 |
| eval_09 | 0.8494 | **0.8872** | 0.8707 | −0.0378 | −0.0213 |
| eval_10 | 0.7687 | **0.8233** | 0.8021 | −0.0546 | −0.0334 |
| eval_11 | 0.7070 | **0.7464** | 0.7308 | −0.0394 | −0.0238 |
| eval_12 | 0.6803 | **0.7244** | 0.7089 | −0.0441 | −0.0286 |
| eval_13 | 0.7376 | **0.8016** | 0.7788 | −0.0640 | −0.0412 |
| eval_14 | 0.8122 | **0.8551** | 0.8383 | −0.0429 | −0.0261 |

Mean 14: **0.7583** vs 010=0.8056 (Δ=−0.0473) and 021=0.7871
(Δ=−0.0288). Wall: 922 s (moderate impairment, like 020).

## Per-seed eval_01
- seed 0: 0.7337
- seed 1: 0.6920
- seed 2: 0.7341

Spread = 0.042 (very large; seed 1 outlier −0.04 below the others).
Confirms pattern: weaker iid anchor → less stable training across
seeds. Spread is now 3.5× normal.

## Pre-registered scorecard
- "022 > 010 by +0.005-0.010 (off-genome anchor monotonic, NEW BEST)":
  **falsified** (worse, not better).
- "022 ≈ 010 within ±0.005 (saturating around uniform)": **falsified**
  (Δ=−0.047, far outside).
- "022 < 010 by 0.005-0.020 (extreme overlaps with CpG-island-like)":
  **partially confirmed in direction, magnitude exceeds prediction**
  (Δ=−0.047, beyond 0.020 ceiling).

## iid composition curve (3 points)
| iid type | composition | distance from hg38 | Δ vs uniform iid |
|----------|-------------|--------------------|------------------|
| hg38-matched (021) | 41% GC | 0pp | −0.018 |
| **uniform (010)** | **50% GC** | **9pp** | **0.000 (baseline)** |
| extreme high-GC (022) | 60% GC | 19pp | −0.047 |

The composition effect is **non-monotonic and asymmetric**, peaked
at uniform (50% GC). Going TOWARD genome composition (021, −0.018)
or AWAY to high-GC (022, −0.047) both hurt, but the high-GC direction
hurts ~2.6× more.

## Theory update — uniform iid is uniquely optimal (max-entropy anchor)
**Refined theory (v6).** Iid value mechanism revised again:
> Iid value is maximized at uniform mononuc composition (50% GC). Both
> deviations from uniform reduce value, but for DIFFERENT reasons:
>   - **Toward genome** (matched composition, 021): loses "off-genome
>     calibration anchor" — sequences look like genomic background
>     and the model can't use them as a clean reference.
>   - **Away from genome to high-GC** (022): the high-GC composition
>     triggers CpG-island-like associations in the model. CpG islands
>     in genome are ~60-70% GC and are distinctive promoter features
>     the model has learned to recognize. High-GC iid sequences are
>     "fake CpG islands" — the model expects regulatory features but
>     finds none → actively confused.
> 
> Uniform is uniquely good because it's:
>   (i) Off-genome enough to anchor (50% GC vs 41% genome)
>   (ii) Below the CpG-island threshold (~60% GC)
>   (iii) Maximum-entropy at the mononucleotide level (no trace of
>        any specific genomic feature, repeat class, or CpG-rich
>        promoter structure).

**Prediction for 30% GC iid (untested but predictable):** intermediate
loss (0.020-0.030). Distance from genome 11pp (slightly more than
uniform's 9pp), but doesn't trigger CpG-island confusion. Possibly
ALSO triggers AT-rich repeat associations (~50% of human genome is
AT-rich repeats: LINEs, SINEs avg 40-45% GC) but those are less
distinctive features than CpG islands.

## Comparison: 022 (high-GC iid) vs 016 (dinuc-shuf cCRE)
Both add components that "look biological but lack signal":
- 022 high-GC iid: composition extreme + no positional structure →
  triggers CpG-island confusion → −0.047
- 016 dinuc-shuf cCRE: composition matched + high dinuc structure →
  preserves cCRE composition stats but destroys motifs → −0.055

Both are similarly damaging (~−0.05). Different failure modes,
similar magnitude. The unifying principle: **adding sequences that
trigger model expectations of regulatory signal but lack real
regulatory features is uniformly bad** — irrespective of whether
the trigger is GC content, dinuc structure, or both.

## What I learned (operational)
1. **Composition is not a smooth axis.** I expected a monotonic
   off-genome effect; reality is a peak at uniform with steep falloff
   in both directions. Should have predicted CpG-island confusion
   beforehand — it's known the model treats high-GC as a regulatory
   signature.
2. **Per-seed spread continues to track library quality.** Spread:
   010=0.012 (healthy), 021=0.030 (matched, weakened anchor),
   022=0.042 (high-GC, broken anchor). Strong correlation with
   anchor strength. Spread is a useful diagnostic.
3. **The iid axis is now well-mapped.** Mass=5K, composition=uniform
   50% GC. Both endpoints constrained. Further iid optimization is
   exhausted.

## What to try next
**023: low-GC iid (30% GC) — symmetry test.** Library: 35K cCRE
7K-each + 5K iid at 30% GC (35% A, 15% C, 15% G, 35% T) + 5K human
+ 5K chicken. Distance from genome 11pp. Tests whether the
high-GC penalty is specifically about CpG-island confusion (in which
case 30% GC should hurt LESS than 60% GC) or about distance from
uniform per se (in which case 30% GC should hurt similarly to 60%
GC).

Pre-registered:
- 023 ≈ 010 within ±0.010 (low-GC has minimal CpG-island confusion;
  AT-rich associations are weak): asymmetric falloff.
- 023 between 021 and 022 (loss 0.020-0.040): partially asymmetric;
  some CpG-island-specific cost, some distance-from-uniform cost.
- 023 ≈ 022 (loss 0.040-0.050): symmetric falloff; distance from
  uniform is what matters, not direction.

Alternatives considered:
- **iid mass curvature (10K iid + drop 5K human-gen)**: probes
  unexplored axis but confounds two changes (mass ↑, human-gen
  removed). Lower information.
- **Coding exons / CNEs / repeat-masked as 5th component**: novel
  source types, but require new data downloads and aren't a clean
  follow-up.
- **Restore 010 baseline as control for re-evaluation**: would test
  evaluation-noise floor but wastes compute.

023 (low-GC symmetry test) cleanly closes out the iid composition
axis. Going with it.
