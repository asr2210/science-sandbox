# 027 — near-cCRE flanking human-gen replaces deep-non-cCRE (35K cCRE + 5K iid + 5K near-flank + 5K chicken)

## Result — near-flank is mildly harmful

| metric  | 027 | 010 | 025 (RC-cCRE) | 016 (dinuc-shuf) | Δ vs 010 |
|---------|-----|-----|---------------|------------------|----------|
| eval_01 | 0.7450 | **0.7599** | 0.7246 | 0.7065 | −0.0149 |
| eval_02 | 0.8402 | **0.8550** | 0.8174 | 0.7976 | −0.0148 |
| eval_03 | 0.8251 | **0.8413** | 0.8009 | 0.7771 | −0.0162 |
| eval_04 | 0.8042 | **0.8140** | 0.7858 | 0.7708 | −0.0098 |
| eval_05 | 0.7448 | **0.7599** | 0.7246 | 0.7066 | −0.0151 |
| eval_06 | 0.8402 | **0.8550** | 0.8171 | 0.7976 | −0.0148 |
| eval_07 | 0.7851 | **0.8044** | 0.7528 | 0.7236 | −0.0193 |
| eval_08 | 0.7248 | **0.7515** | 0.6921 | 0.6631 | −0.0267 |
| eval_09 | 0.8760 | **0.8872** | 0.8538 | 0.8374 | −0.0112 |
| eval_10 | 0.8059 | **0.8233** | 0.7821 | 0.7545 | −0.0174 |
| eval_11 | 0.7318 | **0.7464** | 0.7117 | 0.6941 | −0.0146 |
| eval_12 | 0.7086 | **0.7244** | 0.6887 | 0.6679 | −0.0158 |
| eval_13 | 0.7805 | **0.8016** | 0.7431 | 0.7148 | −0.0211 |
| eval_14 | 0.8403 | **0.8551** | 0.8175 | 0.7978 | −0.0148 |

Mean 14: **0.7895** vs 010=0.8056 (Δ=**−0.0161**). Wall: 1200s.
Per-seed eval_01: seed_0=0.7631, seed_1=0.7301, seed_2=0.7418
(spread 0.033 — moderate, not as alarming as 026's 0.055).

## Pre-registered scorecard
- "027 > 010 by +0.005-0.015 (NEW BEST, proximity-to-cCRE matters)":
  **falsified** (Δ=−0.016, opposite direction).
- "027 ≈ 010 within ±0.010 (any same-species non-cCRE works)":
  **falsified** (Δ=−0.016, just outside band).
- "027 < 010 by 0.005-0.020 (near-flank too cCRE-like, partial-positive)":
  **confirmed in both direction and magnitude** (Δ=−0.016, mid-band).

## "Near-positive" severity ladder

The full data on "how cCRE-adjacent content harms training":

| 4th-slot fill | mean 14 | Δ vs 010 | what it is |
|---------------|---------|----------|------------|
| 010 deep-non-cCRE human | 0.8056 | baseline | random human, ≥200bp from cCRE (mostly >10kb) |
| **027 near-flank human** | **0.7895** | **−0.016** | random human, 200-2000bp from cCRE |
| 025 RC-cCRE | 0.7652 | −0.040 | cCRE itself, reverse-complemented |
| 016 dinuc-shuf cCRE | 0.7426 | −0.063 | cCRE itself, dinucleotide-shuffled |

Monotonic in "how cCRE-like the content is":
- deep-non-cCRE: not cCRE, not near cCRE → optimal anchor
- near-flank: not cCRE, but near cCRE (some shared composition,
  weak motif content from enhancer flanks) → mild harm
- RC-cCRE: real cCRE composition, real motifs (just on opposite
  strand) → moderate harm
- dinuc-shuf cCRE: real cCRE composition, no motifs → severe harm

**The model's training is harmed by ANY content that "looks slightly
like a cCRE but isn't labeled as one."** Slot 4 wants content that
is UNAMBIGUOUSLY non-cCRE — i.e., deep gene-desert or intergenic.

## Theory update (v11) — slot-4 needs UNAMBIGUOUS non-cCRE
**Refined theory:**
> Slot 4 ("same-species non-regulatory anchor") works best when its
> content is unambiguously non-cCRE — i.e., distant enough from any
> cCRE that the model treats it as "different distribution from the
> cCRE component" rather than "near-cCRE confused signal".
>
> The "near-positive" severity ladder is monotonic in shared
> composition/motif content with cCRE:
>   (i) Deep-non-cCRE: ~30%-50% GC, no enhancer-flanking motifs,
>       no shared composition → cleanly different distribution.
>   (ii) Near-flank: ~45-55% GC (enhancer-flanks bias higher GC),
>        weak motif residue → 016 weak adversarial near-positive.
>   (iii) RC-cCRE: matches cCRE composition exactly, retains
>         palindromic motifs → moderate adversarial.
>   (iv) Dinuc-shuf cCRE: matches cCRE 1st+2nd-order composition,
>        no motifs → severe adversarial.

**Implication for design:** the 010 "200bp exclusion + random
sampling" strategy is at or near optimum for slot 4. Tightening
exclusion (less near-content) would marginally help; loosening
(more near-content, like 027) hurts. Excluding even MORE
(e.g., 5kb exclusion) might add ~+0.005 in theory but is hard to
test cleanly without confounding chrom-arm bias.

## What I learned (operational)
1. **The "near-positive" pattern is unified.** RC-cCRE (025),
   dinuc-shuf cCRE (016), and near-flank (027) are all instances
   of the same failure mode. The model has a sharp distinction
   between cCRE and not-cCRE; anything "near" the boundary
   confuses it.
2. **The 010 design has 12 verified joint constraints.** Adding
   slot-4-sampling-strategy = "deep-non-cCRE preferred". Beating
   010 by adjusting any single design axis is now exhausted.
3. **The remaining unexplored axes are second-order.** cCRE WIN
   size, cCRE midpoint vs offset sampling, mixed iid composition,
   iid mass at 4K. Each could yield ~±0.005 at best.

## What to try next

The most promising remaining axis is **iid composition mixing**.
Currently iid is 100% uniform 50% GC. The 021/022/023 composition
sweep showed:
  - Uniform 50% GC: 010 baseline (best alone)
  - hg38-matched 41% GC: 021, −0.018 (worst alone among non-extreme)
  - Low-GC 30%: 023, −0.010
  - High-GC 60%: 022, −0.047 (CpG-island confusion)

Theory says uniform-50% acts as "off-genome calibration" while
hg38-matched acts as "near-genome negative". These are DIFFERENT
calibration mechanisms. Mixing could capture BOTH:

**028: mixed iid (2.5K uniform 50%-GC + 2.5K hg38-matched 41%-GC).**
Library: 35K cCRE + 2.5K iid-uniform + 2.5K iid-hg38-matched +
5K human + 5K chicken = 50K (iid axis split).

Pre-registered:
- 028 > 010 by +0.005-0.015 (NEW BEST): mixing captures two
  distinct calibration mechanisms additively. Possible NEW BEST.
- 028 ≈ 010 within ±0.005: mixing averages the −0.018 (021) and
  0 (010) effects → −0.009 or partial cancellation around 010.
- 028 < 010 by 0.005-0.020: mixing dilutes both calibration
  mechanisms; net loss similar to or below pure-uniform.

Alternatives considered:
- **iid mass at 4K** (with cCRE +1K): closes downside of iid-mass
  curve; predicted ≈ 010 within ±0.005, low-info.
- **cCRE WIN size 150bp or 250bp**: structural change, may break
  prepare.py assumptions; risky.
- **Random offset within cCRE (±50bp)**: positional augmentation
  test; predicted ≈ 010 within ±0.005, low-info.
- **Mouse-cCRE additions**: requires mouse cCRE bed (not present).

028 (mixed iid composition) is the only remaining test that is
both well-grounded in prior theory AND plausibly yields a NEW BEST
through MECHANISM-COMBINATION rather than single-axis optimization.
