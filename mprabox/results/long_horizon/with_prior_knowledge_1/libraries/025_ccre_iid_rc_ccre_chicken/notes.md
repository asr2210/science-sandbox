# 025 — RC-cCRE replaces human-gen (35K cCRE + 5K iid + 5K RC-cCRE + 5K chicken)

## Result — RC-cCRE significantly worse than 010

| metric  | 025 | 010 | 016 | Δ vs 010 |
|---------|-----|-----|-----|----------|
| eval_01 | 0.7246 | **0.7599** | 0.7065 | −0.0353 |
| eval_02 | 0.8174 | **0.8550** | 0.7976 | −0.0376 |
| eval_03 | 0.8009 | **0.8413** | 0.7771 | −0.0404 |
| eval_04 | 0.7858 | **0.8140** | 0.7708 | −0.0282 |
| eval_05 | 0.7246 | **0.7599** | 0.7066 | −0.0353 |
| eval_06 | 0.8171 | **0.8550** | 0.7976 | −0.0379 |
| eval_07 | 0.7528 | **0.8044** | 0.7236 | −0.0516 |
| eval_08 | 0.6921 | **0.7515** | 0.6631 | −0.0594 |
| eval_09 | 0.8538 | **0.8872** | 0.8374 | −0.0334 |
| eval_10 | 0.7821 | **0.8233** | 0.7545 | −0.0412 |
| eval_11 | 0.7117 | **0.7464** | 0.6941 | −0.0347 |
| eval_12 | 0.6887 | **0.7244** | 0.6679 | −0.0357 |
| eval_13 | 0.7431 | **0.8016** | 0.7148 | −0.0585 |
| eval_14 | 0.8175 | **0.8551** | 0.7978 | −0.0376 |

Mean 14: **0.7652** vs 010=0.8056 (Δ=**−0.0404**). Wall: 931s
(moderate impairment, similar to 016).

## Per-seed eval_01
- seed 0: 0.7414
- seed 1: 0.7360
- seed 2: 0.6963

Spread = 0.045. Substantially elevated above 010's 0.012. RC-cCRE
is unstable across seeds — model cannot consistently extract a
useful signal from RC-cCRE entries.

## Pre-registered scorecard
- "025 > 010 by +0.005-0.015 (NEW BEST, model partially strand-aware)":
  **falsified** (Δ=−0.040, much worse).
- "025 ≈ 010 within ±0.010 (RC handled internally, redundant)":
  **falsified** (Δ=−0.040, far outside band).
- "025 < 010 by 0.005-0.020 (RC ≈ dinuc-shuf failure mode)":
  **direction confirmed, magnitude 2× the predicted ceiling**
  (Δ=−0.040 vs predicted −0.005 to −0.020).

## Comparison with 016 (dinuc-shuffled cCRE)
| variant | mean 14 | Δ vs 010 |
|---------|---------|----------|
| 010 (human-gen) | 0.8056 | baseline |
| 025 (RC-cCRE) | 0.7652 | −0.0404 |
| 016 (dinuc-shuf cCRE) | 0.7426 | −0.0630 |

RC-cCRE sits **between dinuc-shuffled cCRE and human-gen**, much
closer to dinuc-shuf than to a clean component. RC-cCRE retains:
- Real motifs (just on opposite strand)
- Real composition / dinuc / k-mer statistics
- Real positional structure (relative motif spacing preserved
  in mirrored order)

But the model treats it as ~70% as harmful as fully shuffled cCRE.

## Theory update (v9) — model is strongly strand-aware, RC ≠ augmentation
**Refined theory:**
> The model has learned **strand-specific motif representations**.
> Reverse-complementing a real cCRE produces a sequence that:
>   (i) Retains real palindromic motifs (small fraction, ~10-20% of
>       TF binding sites are palindromic — CTCF, some bZIPs).
>   (ii) Loses recognition of asymmetric motifs (majority of TFs
>        — e.g., GATA, FOXA, ETS family — have strand-specific
>        binding sites and the model has learned them in canonical
>        orientation).
>   (iii) Creates a "near-cCRE" sequence that the model partially
>        recognizes (real composition, palindromes survive) but
>        whose activity label (low, since RC sequences have no
>        canonical activity assignment in MPRA) conflicts with
>        the model's partial-recognition prediction.
>
> This is worse than dinuc-shuffled (which clearly looks unlike
> a cCRE → model can distinguish) because RC-cCRE is an
> **adversarial near-positive**: it triggers some cCRE-detection
> machinery without being a true cCRE.

**Operational corollary:** the prepare.py training pipeline is
**not performing RC-augmentation**, since if it were, the model
would treat RC-cCRE the same as forward cCRE → ≈ 010. The fact
that RC-cCRE is significantly harmful confirms this.

## Implications for the joint optimum
The 010 design now has 10 verified joint-optimum axes:
- cCRE mass: 35K (sharp peak, 014/015)
- iid mass: 5K (sharp peak, 024)
- iid composition: uniform 50% GC (asymmetric peak, 021/022/023)
- cCRE class balance: 7K-each (near-flat-bottom optimum, 020)
- Cross-species choice: chicken (sharply special, 011/017)
- Cross-species per-species mass: 5K (universal cap, 008/015)
- Cross-species count: saturates at 1 (007/008/009)
- Hard negatives (dinuc-shuf): avoided (016)
- RC-augmentation: avoided (025) — NEW
- 4-component design at 5K each: validated (012)

The "novel high-value 4th component" hypothesis (from 024 notes)
has been falsified for the first natural candidate (RC-cCRE).
Real-genomic cross-species sequences appear uniquely well-suited
as the 4th component.

## What I learned (operational)
1. **The model is strand-aware in a meaningful way.** This is
   non-obvious: many sequence-to-activity models RC-augment by
   default. Either (a) prepare.py's training does NOT RC-augment,
   or (b) the model has limited capacity to learn truly strand-
   invariant representations even with augmentation. Either way,
   RC sequences cannot be used as additive training data.
2. **"Synthetic" 4th components are dangerous.** Any 4th component
   that derives from cCRE (RC, shuffle, masking) risks creating
   adversarial near-positives. The 4th component should derive
   from a DIFFERENT distribution (cross-species, off-genome iid,
   different functional class).
3. **The "novel high-value component" search space is narrowing.**
   - Tried: human-gen (small +), mouse-gen (good), chicken-gen
     (best), zebrafish-gen (good), xenopus-gen (good but < chicken),
     dinuc-shuf cCRE (bad), RC-cCRE (bad).
   - Untried: CpG islands, conserved non-coding (phastCons),
     synthetic motif-rich, near-cCRE flanking (50bp from cCRE,
     not 200bp exclusion), other species (turkey/alligator/
     anole/platypus/echidna).

## What to try next

The most promising remaining directions are:

(A) **Replace human-gen with NEAR-cCRE flanking sequences.**
    Currently human-gen excludes within 200bp of any cCRE; this
    is "deep non-cCRE". Sample windows that are 300-1000bp from
    the nearest cCRE — closer to enhancer flanks where some
    weak motif content may exist. Tests whether the gradient
    "deep-non-cCRE → flanking → cCRE" provides an informative
    in-between signal.

(B) **Replace human-gen with platypus genomic.** Platypus
    (ornAna2) is a monotreme — most distant living mammal from
    human (~166 Mya divergence). Sits between mouse (~96 Mya)
    and chicken (~310 Mya). If the chicken result is driven by
    "right amount of evolutionary divergence," platypus should
    beat or tie chicken. If chicken is special for some other
    reason (bird-specific genome composition, regulatory element
    repertoire), platypus underperforms.

(C) **Add 5th component at small mass: 47.5K / 2.5K split.**
    Reduces each existing component proportionally to add a 2.5K
    "candidate" component. If the candidate is high-value, this
    is the lowest-cost test. Bar is high (~+0.005 net to clear).

I'll go with **(B) platypus genomic**: the cross-species axis
is the highest-value historically (chicken added +0.040 in 010),
and platypus is the cleanest test of "what makes chicken work".
If platypus ≈ chicken or > chicken, we have room to grow. If
platypus < mouse (mammals plateau), confirms chicken is special.

Library 026: 35K cCRE 7K-each + 5K iid + 5K human + 5K platypus
ornAna2 = 50K (replaces chicken with platypus, NOT human, to
isolate the platypus effect cleanly against the closest comparable
experiment which is 006: ...iid + human + mouse).

Wait — better design: replace **human** with platypus (preserve
chicken at 5K, since chicken is the proven best). That is:
35K cCRE + 5K iid + 5K platypus + 5K chicken. This tests whether
platypus + chicken stacks better than human + chicken (current
010). Comparable: 013 (mouse + chicken) had Δ=−0.033 vs 010, so
the "non-human in human's slot" question has been measured for
mouse. Platypus is the natural cross-species replacement for
human-gen.

Pre-registered:
- 026 > 010 by +0.005-0.015: platypus brings novel cross-species
  signal stacking with chicken; **POSSIBLE NEW BEST**.
- 026 ≈ 010 within ±0.010: platypus ≈ human in 4th slot, cross-
  species axis caps regardless of which 5K-mass species fills it.
- 026 < 010 by 0.005-0.030: platypus stacks like mouse on chicken
  (013 result), cross-species cap is per-species not per-axis.
