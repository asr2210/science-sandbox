# 022 — cCRE 013 with random-genomic flank

## Design
Each 200bp sequence is built as a chimera:
  [50bp random hg38 main-chrom flank]
  [100bp cognate cCRE region centered on cCRE midpoint]
  [50bp random hg38 main-chrom flank]

The two random flanks come from independent main-chrom positions
that are >=10kb away from any cCRE call. Class composition matches
013 (10K each rare + 2.5K each abundant = 50K).

## Results (mean over 3 seeds)
- eval_01 = **0.7447** (vs 013 0.7477 = **−0.003**)
- mean across 14 evals = **0.7873** (vs 013 0.7900 = **−0.003**)

## Per-eval delta vs 013
01:−0.003 02:−0.004 03:−0.005 04:−0.012 05:−0.003 06:−0.004 07:−0.019
08:**+0.049** 09:−0.014 10:−0.002 11:−0.003 12:−0.002 13:−0.012 14:−0.004

**Essentially tied with 013 on most evals**, modest losses on 4/13/9
(−0.012 to −0.019), and a *gain* on eval_08 (+0.049). Random flank
helps eval_08 — likely because the broader-coverage benchmark
benefits from genome-distributed background context.

## Per-seed eval_01
seed 0: 0.7565  (1290s)
seed 1: 0.7534  (1313s)
seed 2: 0.7242  ( 866s)

SD ≈ 0.018. Same training-time-vs-accuracy pattern (longer training
→ higher accuracy). seed 0 ≥ 013's mean (0.7477).

## Branching outcome
Pre-experiment branches:
- 022 ≈ 013 → flank is scaffold; specific content doesn't matter (yes)
- 022 ≈ 020 → cognate flank specifically matters (no)
- 022 between → both contribute partially (no)

Result: **022 ≈ 013, decisively**. Random flank is essentially
indistinguishable from cognate flank.

## What this updates in the theory

**T17 (REVISED — flank is mostly scaffold, not regulatory signal):**
The cCRE element itself carries the regulatory signal; the
surrounding ~50bp×2 acts as receptive-field context for the model.
ANY DNA in the flank works. This overturns my previous T17
interpretation (which assumed cognate flank carried co-binding
TF / nucleosome / cell-type-specific signal).

**T19 (new — 020's loss was selection bias, not flank loss):**
020 lost 0.058 vs 013 because filtering to ≥200bp-wide cCREs
selects for broader, less-sharp regulatory regions (narrower cCREs
are sharper peaks with more concentrated regulatory content). The
flank-removal interpretation was confounded by width-filter
selection. To cleanly test no-flank, use ALL cCREs with no
artificial filter — 023 will do this.

**T13 (now strongly supported):** The cCRE peak center IS the
regulatory unit. ~100bp around the called midpoint is sufficient
to capture nearly all of 013's signal. ENCODE's cCRE midpoints
land on actual regulatory peaks; the boundary calls are loose.

**T18 (consistent):** Position prior still matters somewhat
(021 lost 0.028) but flank-content does not (022 lost 0.003). The
two effects are independent: position-jitter disrupts a learned
positional anchor; flank-content swap doesn't disrupt anything the
model learns.

**T8 ablation breakdown of 013 — REVISED:**
- Functional class specificity (T13):     baseline
- Rare-class upweighting (T8):            +0.015 over 006
- 100bp cCRE element vs no element:       MOST of the gain over random
- Flank cognate-vs-random:                negligible (~0.003)
- Centered positional prior (T18):        +0.028
The recipe gain comes from cCRE element + class composition +
position, NOT from flanking sequence content.

## Best library so far
**013 cCRE extreme upweight, mean ≈ 0.7900**. Holds.
**022 ≈ 013 within noise** — essentially equivalent. Suggests we
could also build 50K libraries with 100bp cCRE + random flank.

## Process note
spark06 hung again on multi-seed. Re-ran sequentially via single-
seed local mode. seed 0 from spark01 (0.7565) and from local
(0.7565) match exactly — model_seed=0 is deterministic.
Total runtime ~58 min for 3 sequential seeds.

## Most informative next experiment (023)
T19 says 020's loss was selection bias. Test cleanly: take ALL
cCREs (013 composition, no width filter), extract just 50bp around
each cCRE midpoint, pad with 75bp random hg38 flank on each side.
50bp cCRE region + 150bp random = 200bp.
- 023 ≈ 013 → 50bp cCRE peak alone is enough; even smaller
  regulatory unit
- 023 ≈ 022 → 100bp is needed; shrinking to 50bp loses signal
  (and we can pinpoint cCRE region size)
- 023 << 022 → cCRE region needs >50bp; the regulatory unit is
  larger than just the midpoint

This finds the minimum cCRE region that captures 013's signal,
and confirms T17 revision under different region sizes.
