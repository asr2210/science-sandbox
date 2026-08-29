# 014 — cCRE (40K) + iid (5K) + chicken (5K), NO HUMAN, NO MOUSE

## Result — SURPRISE regression, cCRE saturates BEFORE 40K
| metric  | 014 | 010 | 013 | Δ vs 010 |
|---------|-----|-----|-----|----------|
| eval_01 | 0.7285 | **0.7599** | 0.7523 | −0.0314 |
| eval_02 | 0.8196 | **0.8550** | 0.8485 | −0.0354 |
| eval_03 | 0.8020 | **0.8413** | 0.8332 | −0.0393 |
| eval_04 | 0.7888 | **0.8140** | 0.8103 | −0.0252 |
| eval_05 | 0.7284 | **0.7599** | 0.7521 | −0.0315 |
| eval_06 | 0.8198 | **0.8550** | 0.8486 | −0.0352 |
| eval_07 | 0.7531 | **0.8044** | 0.7956 | −0.0513 |
| eval_08 | 0.7015 | **0.7515** | 0.7442 | −0.0500 |
| eval_09 | 0.8579 | **0.8872** | 0.8827 | −0.0293 |
| eval_10 | 0.7811 | **0.8233** | 0.8181 | −0.0422 |
| eval_11 | 0.7155 | **0.7464** | 0.7391 | −0.0309 |
| eval_12 | 0.6903 | **0.7244** | 0.7165 | −0.0341 |
| eval_13 | 0.7419 | **0.8016** | 0.7889 | −0.0597 |
| eval_14 | 0.8200 | **0.8551** | 0.8488 | −0.0351 |

Mean 14: **0.7677** vs 010=0.8056 (−0.0379) vs 013=0.7985 (−0.0308). Wall: 1274 s.

## Per-seed eval_01
- seed 0: 0.7543 (basically tied with 010 seed 0)
- seed 1: 0.6945 (catastrophic seed)
- seed 2: 0.7368

Spread = 0.0598, 6× wider than 010's 0.010, comparable to 012's 0.052.

## Pre-registered scorecard
- "014 > 010 by ≥ +0.005 (cCRE returns continue past 35K, NEW BEST)":
  **strongly falsified** (Δ −0.038).
- "014 ≈ 010 (±0.005) (cCRE 35→40 ≈ human-gen loss)": **falsified**.
- "014 < 010 by 0.005-0.015 (cCRE saturates by 35K AND human-gen
  meaningful)": falsified (regression bigger than this).
- "014 < 010 by > 0.015 (cCRE 40K actively worse OR human critical)":
  **confirmed**, with magnitude (−0.038) bigger than expected from
  either factor alone.

## Disentangling the −0.038
Two factors moved between 010 and 014:
  (a) cCRE 35K → 40K (+5K cCRE)
  (b) human-genomic 5K → 0K (−5K human-gen)

From 013's isolation (010 → 013 = drop human-gen, add mouse-gen, ≈0
species stack value): human-gen contribution ≈ +0.007 mean.

Therefore: cCRE 35→40K contribution ≈ −0.038 − (−0.007) = **−0.031 mean**.

cCRE elasticity past 35K is **sharply negative**, not zero or weakly
positive. This reverses the implicit assumption from the 008-006
contrast that "cCRE elasticity is roughly constant near 35K". The
function is concave with a peak near 35K — adding more cCRE actively
hurts, presumably by giving the model excess opportunity to overfit
narrow cCRE-specific features at the expense of general regulatory
grammar.

Alternative interpretation: human-genomic value scales with library
diversity (just like iid did between 002 and 012). If human-gen is
worth ~+0.025 in this 4-axis context, then cCRE 35→40 is roughly flat.
Either way, the lesson is: don't push cCRE past 35K.

## Per-seed instability is the second story
Seed 1 (0.6945) is wildly off — 6 std-devs from 010's seed spread.
The library is fragile without human-genomic. Hypothesis: human-gen
provides a stabilizing "human-distribution baseline" that lets the
model anchor non-cCRE human regulatory grammar; without it, training
on 80% cCRE + 10% iid + 10% chicken can produce a model that
over-fits cCRE motif statistics in training-instability-sensitive
ways (high seed variance).

This is the second time we've seen a wide seed spread coincide with a
mean regression: 012 (no iid) and 014 (no human-gen). Suggests **both
iid AND human-gen serve stabilization roles** — iid as off-genome
anchor, human-gen as on-genome non-cCRE anchor. Removing either
destabilizes training across seeds, not just the mean.

## Theory update — cCRE plateau at ≈35K, human-gen has stabilizing role
> 4-axis decomposition (this study, post-014):
>   - cCRE backbone: PEAKS NEAR 35K. Slope ≈ −0.005 going down,
>     ≈ −0.006 going up. Roughly concave in the 30-40K window.
>     Don't push past 35K.
>   - iid: REQUIRED anchor at 5K when cross-species present (~+0.05).
>     Stabilizes seed variance.
>   - Human non-cCRE genomic: not just +0.007 mean — also a STABILIZER.
>     Removing it widens seed spread 6× and may have larger mean
>     contribution in 4-axis libraries than 013's isolation suggested.
>   - Per-species cross-species: hump-shaped, peak chicken (+0.023).
>     Caps at ONE species at 5K mass.
>
> Best 4-axis remains 010 (35K cCRE + 5K iid + 5K human + 5K chicken).

## What I learned (operational)
1. **Pushing a known-good axis past its proven range can backfire
   sharply.** cCRE elasticity going UP from 35K isn't symmetric with
   elasticity going DOWN. Plateaus end on both sides. Same pattern
   we saw for cross-species mass (saturates at 5K from below, then
   008 showed pushing to 10K hurts).
2. **Seed spread is a leading indicator of library fragility.** Both
   012 and 014 had ~5-6× wider seed spread than 010, and both showed
   sharp mean regressions. Wide spread = lost a stabilizing axis.
3. **Component values cannot be subtracted naively across configurations
   even with the cleanest single-variable swap.** 010→013 gave
   human-gen ≈ +0.007, but 014's gap suggests it's worth more — likely
   because in 014, human-gen would have to anchor the library in the
   absence of mouse, which it didn't have to do in 013. Context.

## What to try next
**015: test cCRE saturation point more precisely.** 30K cCRE + 5K iid
+ 5K human + 10K chicken (mouse=0, cCRE=−5K from 010, chicken=+5K).
- Tests: (a) does pushing chicken to 10K help (cross-species mass past
  5K), (b) does cCRE 30K hold value when freed for cross-species mass.
- Predicted falsifiable: 008 found 10K of one species hurt, but in 008
  the species was mouse and the gain went to no other axis. In 015 we
  use chicken (proven best species) AND the 5K is freed for chicken,
  so the test is cleaner.
- 015 > 010 by ≥ +0.005: chicken 10K stacks (cross-species past 5K
  saturation). Likely if hump's PEAK is at chicken specifically.
- 015 ≈ 010 (±0.005): 5K is the chicken plateau too.
- 015 < 010 by > 0.005: cross-species saturates universally at 5K AND
  cCRE 35K is critical. Regress to 010.

Alternative 015: 35K cCRE + 5K iid + 5K human + 5K xenopus or
platypus (test "near chicken" amniote candidates from 011's hump
theory). This is more incremental.

I'll go with the chicken-10K version for 015. Higher-information
about the saturation mechanism.