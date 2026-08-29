# 018 — DHS rare-component upweighted (013 principle on DHS)

## Design
Apply 013's rare-class upweighting principle to the Meuleman DHS
Index. Use 009's quality filter (mean_signal >= q75 AND
numsamples >= 5; 681K filtered elements). Group by primary NMF
component (16 cell-type vocabularies). Sort by post-filter pool
size; smallest 8 = rare (5000 each = 40K), largest 8 = abundant
(1250 each = 10K). 4:1 rare:abundant ratio matches 013.

200bp centered on DHS summit (same as 008/009).

## Results (mean over 3 seeds)
- eval_01 = **0.6911** (vs 013 0.7477 = **−0.057**)
- mean across 14 evals = **0.7331** (vs 013 0.7900 = **−0.057**)

## Per-eval delta vs 013
01:−0.057 02:−0.059 03:−0.061 04:−0.068 05:−0.057 06:−0.058 07:−0.067
08:−0.029 09:−0.078 10:−0.032 11:−0.055 12:−0.053 13:−0.063 14:−0.058

**Loses on ALL 14 evals**, by 0.029-0.078. Average −0.057.

Comparison to other DHS recipes:
- 008 DHS uniform:        0.7297
- 009 DHS filtered:       0.7500
- 018 DHS rare-component: 0.7331  (≈ 008, *worse* than 009)

The rare-class principle that gained +0.028 going from 006 to 013 in
cCRE LOSES 0.017 going from 009 to 018 in DHS. The principle does
not transfer.

## Across-seed
eval_01: 0.6807 / 0.7251 / 0.6675 → SD ≈ 0.025 (vs 013's 0.008).
Higher variance, similar to 016.

## Branching outcome
Pre-experiment branches:
- 018 > 013 → universal principle (no)
- 018 ≈ 013 → atlas-agnostic (no)
- 018 < 013 → DHS less informative even with rebalancing (yes)

Result: **018 ≪ 013, principle does NOT generalize cross-atlas.**

## What this updates in the theory
**T13 (strongly reinforced):** Functional specificity, not pool size,
drives upweighting gains. cCRE classes are *regulatory-mechanism*
labels (PLS=promoter, CA-CTCF=insulator, CA-TF=TF-binding, etc.) —
each rare class encodes a structurally distinct sequence grammar.
DHS NMF components are *cell-type-loading* labels (Lymphoid,
Cardiac, Neural, etc.) — biologically meaningful but not
mechanistically distinct at the sequence level. Two DHS sites in
"Cardiac" vs "Lymphoid" can have nearly identical regulatory
sequence; two cCREs in "PLS" vs "dELS" likely cannot.

**T15 (new — atlas labels matter):** Stratification gains depend on
whether the atlas labels partition sequences along the *axis the
model needs to learn*. cCRE class boundaries are aligned with
regulatory-mechanism sequence syntax (what the model needs);
DHS NMF components are aligned with tissue activity (what the model
already infers from sequence + cell type input). Upweighting along
the wrong axis adds noise, not signal.

**T7 (refined — cCRE > DHS holds even under matched preprocessing):**
With identical filter (q75 signal + ≥5 samples) and identical
upweighting principle, 018 (DHS) << 013 (cCRE). The cCRE atlas
inherently provides a more informative partition for this task,
beyond peak-quality differences.

## Best library so far
**013 cCRE extreme upweight (10K/2.5K), mean ≈ 0.7900**. Holds.

## Process note
spark06 had a persistent NFS hang that blocked the multi-seed
parallel pipeline. Ran each seed sequentially via single-seed mode
on the local GPU; assembled the averaged result.json manually.
Total runtime 2057s = 3 × ~10 min sequentially.

## Most informative next experiment (019)
**Mix 013 with high-quality DHS (009-style).** 25K from 013 (scaled
by 0.5: 5K each rare, 1.25K each abundant) + 25K from filtered DHS
(uniform from the 681K q75/≥5 pool). Tests whether DHS adds any
information *on top of* cCRE.
- 019 > 013 → DHS adds independent signal even when atlas-stratified
  alone is weak; combination > pure cCRE
- 019 ≈ 013 → DHS is redundant given cCRE; cCRE alone sufficient
- 019 < 013 → DHS dilutes cCRE quality (consistent with 007 = strat
  + random failing); pure 013 is best

This cleanly tests "cross-atlas signal addition" — different from
cross-atlas principle generalization (018).
