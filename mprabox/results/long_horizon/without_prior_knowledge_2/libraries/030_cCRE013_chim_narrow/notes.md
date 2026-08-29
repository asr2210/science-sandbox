# 030 (final) — chimera 022 design with narrow cCRE filter

## Design
022's chimera: 50bp random hg38 flank + 100bp cognate cCRE + 50bp
random hg38 flank = 200bp. 013 class composition (10K rare + 2.5K
abundant). cCREs filtered to narrowest ceil(N*1.10) per class
(width-ranked).

Resulting per-class max widths:
- PLS:        207bp (from 47K → narrowest 11K)
- CA-CTCF:    163bp (from 126K → narrowest 11K)
- CA-TF:      282bp (from 26K → narrowest 11K — tightest pool)
- CA-H3K4me3: 183bp (from 79K → narrowest 11K)
- pELS:       151bp (from 249K → narrowest 2.75K)
- dELS:       150bp (from 1.47M → narrowest 2.75K)
- CA:         154bp (from 246K → narrowest 2.75K)
- TF:         150bp (from 105K → narrowest 2.75K)

So 6/8 classes filtered to <=183bp; 2 classes (CA-TF and PLS)
slightly broader. Compared to 022's natural-width pools (median
~240-320bp), this is aggressively narrow.

## Results (mean over 3 seeds)
- eval_01 = **0.6990** (vs 022 0.7447 = **-0.046**, vs 013 0.7477 = -0.049)
- mean across 14 evals = **0.7369** (vs 022 0.7873 = **-0.050**,
  vs 013 0.7900 = -0.053)
- eval_08 = **0.6901** (vs 022 0.7529 = **-0.063**, vs 013 0.7044 = -0.014)

030 is below BOTH 022 and 013 on every axis — narrow x chimera shows
clear ANTI-SYNERGY.

## Per-eval delta vs 022
01:-0.046 02:-0.048 03:-0.050 04:-0.053 05:-0.046 06:-0.048 07:-0.053
08:-0.063 09:-0.060 10:-0.049 11:-0.045 12:-0.045 13:-0.055 14:-0.048
ALL evals lost ~0.045-0.063 vs 022. Universal drop, eval_08 worst hit.

## Per-seed eval_01
seed 0 (spark01): 0.7270
seed 1 (local):   0.6983
seed 2 (spark04): 0.6716
SD ≈ **0.028** (normal range — NOT the degenerate fast-converge
fingerprint of 024/029 which had SD ≈ 0.001-0.004). Time 817s
(also normal). The model trained healthily but on less-informative
data.

## Branch outcome
- 030 mean ≥ 0.79 AND eval_08 ≥ 0.74 → new top library → **NO**
- 030 mean ≈ 022, eval_08 ≈ 022 → narrow filter redundant → **NO**
- 030 mean < 022 by 0.005+ → narrow x chimera anti-synergy →
  **YES, -0.050**

## What this teaches

**T30 (new — narrow-width-extreme selection hurts even with chimera):**
Combining T22 (chimera eval_08 boost) with T27 (narrow more
informative per-instance) does not yield additive gains. Aggressively
narrow cCRE selection (<=200bp for most classes) loses 0.05 even
when chimera scaffolding is preserved.

**T27 (REVISED — width has a sweet spot, not a monotone):** 028
showed forcing equal counts across width quartiles (lifting broad
cCREs) HURT (-0.041). I read this as "narrow > broad per-instance."
But 030 now shows that going to the narrow EXTREME also hurts
(-0.050 vs the natural-width chimera 022). Both width extremes
hurt; the natural class-pool width distribution that 013 captures
is at a sweet spot. The truth is:
- Narrow cCREs (~150-200bp) are well-localized peaks but may be
  weakly-called and atypical
- Broad cCREs (~300-350bp) span context that dilutes the signal
- The natural per-class width distribution mixes both in
  approximately optimal proportion

**T22 mechanism (refined):** 022's chimera works by REPLACING the
naturally-selected flank context with random scaffolding while
preserving a 100bp cognate window. When the cognate cCRE is at
its natural width (median ~250-320bp), the 100bp window samples
the cCRE peak. When cognate is forced to be narrow (<200bp), the
100bp window may overshoot the cCRE entirely — partially capturing
the cCRE's natural genomic edge context that we'd intended to remove.
So narrow cCREs + chimera = leakage of the wrong kind.

**T31 (new — feature interaction is common):** Multiple "good
ideas" don't compose: 026 (chimera + full-cCRE 50/50) failed
(T24); 030 (chimera + narrow filter) failed (T30). Each modification
to 013/022's recipes individually has a clear effect, but
combining modifications usually gives sub-additive or anti-synergistic
results. The library design space is non-additive — trust empirical
combinations, not analytic ones.

## Final ranking (mean across 14 evals)
**013 cCRE extreme upweight    0.7900  ← BEST overall**
**022 cCRE 013 random-flank    0.7873  ← BEST eval_08 (0.7529)**
027 cCRE 013 DHS-quality       0.7859
012 cCRE rare-upweight         0.7819
015 cCRE bracket 11K/1.5K      0.7802
023 cCRE 013 50bp core         0.7784
019 cCRE 013 + DHS mix         0.7768
006 stratified cCRE            0.7754
026 cCRE 013 + 022 dual        0.7716
011 cCRE 3-superclass          0.7715
016 cCRE 1/sqrt-pool           0.7694
007 cCRE strat + random        0.7672
002 cCRE uniform               0.7619
021 cCRE 013 off-center        0.7617
017 cCRE 013 + motif aug       0.7595
009 DHS filtered               0.7500
028 cCRE 013 width-strat       0.7486
010 cCRE TF-strat              0.7493
025 cCRE 013 RC aug            0.7466
**030 cCRE 013 chim narrow     0.7369  ← anti-synergy**
018 DHS rare-component up      0.7331
001 random uniform             0.7321
020 cCRE 013 no-flank          0.7317
008 DHS uniform                0.7297
029 cCRE 013 160bp/20bp chim   0.7291
024 cCRE 013 + random mix      0.7235
014 cCRE rare-only             0.7155
005 random genomic             0.7016
004 motifs in random           0.6824
003 dinuc-shuf cCRE            0.6595

## Final recommendation
**013 (cCRE extreme upweight)** for overall mean (0.7900). Within
each class draw uniformly from the natural pool. Class composition:
10K each of {PLS, CA-CTCF, CA-TF, CA-H3K4me3} + 2.5K each of
{pELS, dELS, CA, TF}. 200bp centered on cCRE midpoint. No flanks,
no augmentation, no width filter.

If eval_08 is critical, **022 (chimera 100bp cognate + 50bp random
hg38 flank each side, 013 class composition)** trades 0.003 mean
for +0.049 on eval_08.
