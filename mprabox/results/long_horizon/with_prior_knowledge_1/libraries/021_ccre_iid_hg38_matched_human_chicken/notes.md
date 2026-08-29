# 021 — iid composition test (35K cCRE + 5K hg38-mononuc-matched iid + 5K human + 5K chicken)

hg38 mononuc freq from chr1: A=0.2910, C=0.2085, G=0.2087, T=0.2918
(GC=0.4172, representative of whole-genome ~41% GC).

## Result — hg38-matched iid is worse than uniform iid: composition matters
| metric  | 021 | 010 | Δ vs 010 |
|---------|-----|-----|----------|
| eval_01 | 0.7439 | **0.7599** | −0.0160 |
| eval_02 | 0.8383 | **0.8550** | −0.0167 |
| eval_03 | 0.8236 | **0.8413** | −0.0177 |
| eval_04 | 0.8000 | **0.8140** | −0.0140 |
| eval_05 | 0.7439 | **0.7599** | −0.0160 |
| eval_06 | 0.8384 | **0.8550** | −0.0166 |
| eval_07 | 0.7835 | **0.8044** | −0.0209 |
| eval_08 | 0.7187 | **0.7515** | −0.0328 |
| eval_09 | 0.8707 | **0.8872** | −0.0165 |
| eval_10 | 0.8021 | **0.8233** | −0.0212 |
| eval_11 | 0.7308 | **0.7464** | −0.0156 |
| eval_12 | 0.7089 | **0.7244** | −0.0155 |
| eval_13 | 0.7788 | **0.8016** | −0.0228 |
| eval_14 | 0.8383 | **0.8551** | −0.0168 |

Mean 14: **0.7871** vs 010=0.8056 (Δ=−0.0185).
Wall: 1285 s (normal training, no early-stop pathology).

## Per-seed eval_01
- seed 0: 0.7372
- seed 1: 0.7320
- seed 2: 0.7624

Spread = 0.030 (larger than usual 0.012). Seed 2 is an outlier on the
high side — suggests a slightly less stable training regime, possibly
because the iid component is closer to genome composition and provides
weaker calibration anchor.

## Pre-registered scorecard
- "021 ≈ 010 within ±0.005 (composition doesn't matter)":
  **falsified** (Δ=−0.0185, well outside ±0.005).
- "021 > 010 by +0.005-0.015 (hg38-matched is BETTER, NEW BEST)":
  **falsified** (worse, not better).
- "021 < 010 by 0.005-0.020 (hg38-matched is WORSE, uniform anchor
  better)": **CONFIRMED** (loss = 0.018, in range).
- "021 << 010 by > 0.030 (hg38-matched fully erases anchor)":
  falsified (loss is partial, not catastrophic).

## Decomposition of iid value
| component | Δ |
|-----------|------|
| Total iid value (012: removing iid entirely costs −0.056) | +0.056 |
| "Off-genome composition" component (021: matching genome composition costs −0.018) | +0.018 |
| "Positional randomness / no motif content" component (residual) | +0.038 |

So the iid value (+0.056 total) decomposes into:
- **~32% from off-genome composition** (uniform 50% GC vs genome 41% GC).
  Making iid look like genome composition removes this ~+0.018.
- **~68% from positional randomness / no motif content** (uniform-by-
  position, no biological pattern, no inter-base dependencies).
  This survives composition matching.

## Theory update — iid value is dual-source
**Refined theory (v5).**
> Iid sequences contribute ~+0.056 to mean accuracy via TWO mechanisms:
>   (i) **Off-genome composition anchor (~+0.018, 32%):** distinct GC
>       content (50% vs 41%) calibrates the model's sequence-likelihood
>       prior — anchors "what does sequence look like when there's no
>       biology".
>   (ii) **Positional randomness anchor (~+0.038, 68%):** no positional
>        structure / no motif content / no inter-base dependencies —
>        anchors "what does sequence look like when there's no
>        regulatory grammar".
> Both are calibration anchors but operate on different statistical
> dimensions.

This is consistent with the dinuc-shuffled-cCRE result (016: −0.055
from adding 5K dinuc-shuffled cCRE). Dinuc-shuffled = preserves
composition AND dinuc transitions, removes only higher-order structure.
In our framework: dinuc-shuf has full genome composition AND high
positional structure (dinuc patterns) → no anchor value AND actively
confusing → −0.055.

Meanwhile uniform iid: no composition match AND no positional structure
→ both anchors active → +0.056. The dinuc-shuf and uniform-iid sit
at opposite ends of the (composition, structure) plane.

## What I learned (operational)
1. **Component values are decomposable.** By varying ONE sub-property
   (composition) while holding mass and source-type fixed, the iid
   value decomposed cleanly into two additive pieces. Same approach
   can be applied to other components (e.g., what's the "essence" of
   chicken's value? Composition? Genome size? Amniote regulatory grammar?).
2. **Negative results have positive theoretical implications.** 021
   didn't yield a NEW BEST, but it cleanly partitioned iid value into
   two mechanisms, which couldn't be done from 010+012 alone.
3. **Seed variance grew when anchor weakened.** Per-seed spread on
   eval_01 went from typical 0.012 (010) to 0.030 (021). Weaker
   off-genome anchor → less stable training. Spread may be a
   secondary signal of library quality.
4. **42% GC for chr1 ≈ whole-genome composition.** Sampling from
   chr1 (250 Mb) gives a representative reference for hg38
   composition without computational overhead of full genome.

## What to try next
**022: extreme high-GC iid push.** Test if the off-genome composition
anchor effect is monotonic in composition distance. Library: 35K cCRE
7K-each + 5K iid at 60% GC (30% C, 30% G, 20% A, 20% T) + 5K human
+ 5K chicken = 50K. Distance from genome composition: 19pp (vs
uniform's 9pp).

Pre-registered:
- 022 > 010 by +0.005-0.010: off-genome anchor is monotonic in
  composition distance. Going further off-genome pays modestly.
  **POSSIBLE NEW BEST** (small margin, ~0.005).
- 022 ≈ 010 within ±0.005: anchor effect saturates around uniform
  composition. Further GC-extreme adds no additional value.
- 022 < 010 by 0.005-0.020: extreme composition makes iid look like
  CpG islands (~70% GC) or low-complexity sequence, REDUCING anchor
  value. Composition effect is non-monotonic with a peak near uniform.

Alternatives considered:
- **Low-GC iid (e.g., 30% GC)**: distance 11pp from genome, less
  extreme than 60% GC, and AT-rich extremes overlap with introns and
  gene deserts (40-42% GC). Less clean off-genome push.
- **Mix uniform + matched iid (2.5K each)**: tests linearity, but
  predicted result is exactly halfway by additivity → low information.
- **Larger uniform iid (7.5K, with 32.5K cCRE)**: probes mass
  curvature but confounds with cCRE reduction.
- **Coding exons / TSSs / CpG islands as a 5th category**: novel
  source types but moderate-overlap with cCRE classes; less clean
  signal.

022 (extreme high-GC iid) is the cleanest test of off-genome anchor
monotonicity. Going with it.
