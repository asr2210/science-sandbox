# 026 — platypus replaces human-gen (35K cCRE + 5K iid + 5K platypus + 5K chicken)

## Result — platypus is worse than human OR mouse in the 4th slot

| metric  | 026 | 010 | 013 (mouse+chk) | Δ vs 010 |
|---------|-----|-----|-----------------|----------|
| eval_01 | 0.7392 | **0.7599** | 0.7523 | −0.0207 |
| eval_02 | 0.8331 | **0.8550** | 0.8485 | −0.0219 |
| eval_03 | 0.8175 | **0.8413** | 0.8332 | −0.0238 |
| eval_04 | 0.7974 | **0.8140** | 0.8103 | −0.0166 |
| eval_05 | 0.7391 | **0.7599** | 0.7521 | −0.0208 |
| eval_06 | 0.8334 | **0.8550** | 0.8486 | −0.0216 |
| eval_07 | 0.7753 | **0.8044** | 0.7956 | −0.0291 |
| eval_08 | 0.7245 | **0.7515** | 0.7442 | −0.0270 |
| eval_09 | 0.8695 | **0.8872** | 0.8827 | −0.0177 |
| eval_10 | 0.8001 | **0.8233** | 0.8181 | −0.0232 |
| eval_11 | 0.7262 | **0.7464** | 0.7391 | −0.0202 |
| eval_12 | 0.7026 | **0.7244** | 0.7165 | −0.0218 |
| eval_13 | 0.7692 | **0.8016** | 0.7889 | −0.0324 |
| eval_14 | 0.8334 | **0.8551** | 0.8488 | −0.0217 |

Mean 14: **0.7829** vs 010=0.8056 (Δ=**−0.0227**). Wall: 1333s
(normal). Per-seed eval_01: seed_0=0.7033, seed_1=0.7561,
seed_2=0.7581 (spread = **0.055** — very high, alarming).

## Per-seed analysis
- seed 0: 0.7033 (catastrophically low, like 016/018)
- seed 1: 0.7561 (close to 010 baseline)
- seed 2: 0.7581 (close to 010 baseline)

This 0.055 spread is the **largest of any non-broken library**. It
mirrors the 023 SIGPIPE incident in shape (one bad seed pulling
mean down) but is real — all three sequence files generated cleanly
with 50K each. Platypus genomic is intrinsically unstable training
data, suggesting either:
  (a) The platypus genome quality / repeat content varies sharply
      between samples, producing highly variable signal.
  (b) Random sampling lands on extremely AT-rich or repeat-dense
      regions in seed 0.

## Pre-registered scorecard
- "026 > 010 by +0.005-0.015 (NEW BEST, evolutionary distance theory)":
  **falsified** (Δ=−0.023, much worse).
- "026 ≈ 013 (platypus = mouse, mammal grouping)": **partially
  confirmed** (026 < 013 by 0.012; platypus worse than mouse, not
  identical).
- "026 ≈ 010 within ±0.005 (cross-species saturation theory)":
  **falsified** (Δ=−0.023, far outside band).

## 4th-component value ranking (with chicken at 5K in 5th slot)

| 4th-slot fill | mean 14 | Δ vs 010 |
|---------------|---------|----------|
| **010 human-gen** (same-species, 200bp cCRE excl) | **0.8056** | **baseline** |
| 013 mouse-gen | 0.7945 | −0.0111 |
| 026 platypus-gen | 0.7829 | −0.0227 |
| 025 RC-cCRE (synthetic) | 0.7652 | −0.0404 |
| 016 dinuc-shuf cCRE (synthetic) | 0.7426 | −0.0630 |

The ordering is **monotonic in evolutionary distance from human
ONLY for real-genomic 4th slots**, NOT in distance from chicken:
- human (0 Mya from itself) — best
- mouse (96 Mya) — next
- platypus (166 Mya) — third
- chicken (310 Mya) — would presumably be worst given trend, but
  not testable in 4th slot since chicken occupies slot 5

**Synthetic 4th slots (RC, dinuc-shuf) are catastrophic regardless
of "distance" — they are adversarial near-positives.**

## Theory update (v10) — the 4th slot wants SAME-SPECIES background, not cross-species

**Refined theory:**
> The 010 design has TWO non-cCRE genomic slots performing distinct
> roles:
>   - **Slot 4 (5K human-gen, 200bp cCRE-excluded):** "Same-species
>     non-cCRE chromatin background." Helps the model distinguish
>     "what cCRE looks like" from "what generic human DNA looks like
>     when it ISN'T regulatory". Cross-species fillers degrade this
>     because they bring cross-species composition + repeat-content
>     signal that the model treats as "non-human" rather than
>     "non-regulatory-human". Value: ~+0.011 over removing it.
>   - **Slot 5 (5K chicken-gen):** "Cross-species evolutionary signal."
>     Adds motif diversity from a sufficiently-distant species that
>     CONSERVED motifs become salient (orthologous TFs across
>     amniotes) while non-conserved sequence becomes "negative
>     calibration". Value: ~+0.040 over removing it.
>
> The two slots are NOT interchangeable. Filling slot 4 with cross-
> species (mouse, platypus) trades a high-value same-species anchor
> for redundant cross-species signal that's already saturated by
> chicken. Net: −0.011 to −0.023.

**Why platypus < mouse < human in slot 4?** Compositional drift +
repeat density. Mouse genome is somewhat similar to human (~55%
genome shares synteny). Platypus diverged ~166 Mya AND has a
fragmented assembly with high repeat content — its "background"
sequence is qualitatively further from human background than
mouse's. This degrades slot 4's role as a "same-species non-cCRE
calibration anchor".

**The 010 design now has 11 verified joint-optimum constraints.**

## What I learned (operational)
1. **Slot 4 and slot 5 of the 010 design are NOT symmetric.** I had
   assumed "any non-cCRE genomic 5K" could fill slot 4. Wrong:
   slot 4 needs same-species; slot 5 needs cross-species; swapping
   loses on both ends.
2. **Per-seed spread is a strong quality signal.** The 0.055 spread
   on 026 reveals platypus-genomic instability that the mean alone
   doesn't show. Always inspect per-seed spread before pre-registering
   theory updates.
3. **The "novel high-value 4th component" search is essentially
   closed.** Tested in slot 4: human (best), mouse (−0.011),
   platypus (−0.023), RC-cCRE (−0.040), dinuc-shuf cCRE (−0.063).
   None of the alternatives has cleared 010. The remaining
   options are CpG-islands, phastCons, or near-cCRE flanking
   (which probes the SUB-SLOT structure of human-gen sampling).

## What to try next

The "same-species background" finding suggests that the value of
slot 4 may come from a SPECIFIC sub-distribution of human genome,
not all-human-non-cCRE. **027: near-cCRE flanking human genomic.**
Sample human windows at distances 200-2000bp from the nearest cCRE
(currently 010 uses 200bp+, sampling deep-non-cCRE which is mostly
gene deserts and intergenic).

Library 027: 35K cCRE 7K-each + 5K iid + 5K near-cCRE-flank human
+ 5K chicken = 50K. Replaces the 010 deep-non-cCRE sampling
strategy with proximity-restricted sampling.

Pre-registered:
- 027 > 010 by +0.005-0.015 (NEW BEST): proximity-to-cCRE matters,
  near-cCRE flanks provide weak-motif background that informs the
  model's chromatin-context discrimination.
- 027 ≈ 010 within ±0.010: distance-from-cCRE doesn't matter for
  slot 4; uniform random non-cCRE is sufficient.
- 027 < 010 by 0.005-0.020: near-cCRE flanks are too "cCRE-like"
  and create a partial adversarial-near-positive effect (analogous
  to RC-cCRE but milder).

Alternatives considered:
- **CpG islands**: requires UCSC cpgIslandExt bed download
  (small, ~1MB) and CpG islands overlap PLS heavily — would
  duplicate cCRE component.
- **phastCons-conserved non-coding**: requires phastCons download
  (~1GB) — heavy.
- **Mix of human + small cross-species in slot 4 (e.g., 4K human
  + 1K dog)**: probes additivity, but predicted near-zero.
- **Probe slot 5 (chicken) variants**: chicken is proven best;
  unlikely to find improvement.

027 (near-cCRE flanking human) is the highest-information test
remaining that uses existing data and probes a specific sub-axis
of the proven-best 010 design.
