# 017_pels_random_offset — notes

## Design
50K unique pELS (no replacement). Window center sampled
uniformly from `[start, end]` of each cCRE rather than fixed
at the cCRE midpoint. Same 200bp window length, same pool.
Tests positional augmentation as an alternative to RC (016)
and central-only (012).

## Hypothesis
- (A) "Central is privileged": cCRE midpoint contains the
  densest signal; off-center windows dilute with flanking.
  mean < pELS012 (0.758).
- (B) "Position is noise": grammar uniform across element;
  mean ≈ pELS012.
- (C) "Diversity wins": positional variation acts as natural
  augmentation; mean > pELS012.

## Result vs. pELS-only

| eval | pELS012 | offs017 | Δ      |
|------|---------|---------|--------|
| 01   | 0.7203  | 0.7034  | -0.017 |
| 02   | 0.8129  | 0.7956  | -0.017 |
| 03   | 0.7958  | 0.7816  | -0.014 |
| 04   | 0.7603  | 0.7421  | -0.018 |
| 05   | 0.7203  | 0.7035  | -0.017 |
| 06   | 0.8133  | 0.7961  | -0.017 |
| 07   | 0.7489  | 0.7346  | -0.014 |
| 08   | 0.6844  | 0.6604  | -0.024 |
| 09   | 0.8238  | 0.8049  | -0.019 |
| 10   | 0.7729  | 0.7485  | -0.024 |
| 11   | 0.7083  | 0.6917  | -0.017 |
| 12   | 0.6853  | 0.6721  | -0.013 |
| 13   | 0.7473  | 0.7384  | -0.009 |
| 14   | 0.8129  | 0.7952  | -0.018 |

Mean: pELS012 0.758, **offs017 0.741, Δ=-0.017**.

## Interpretation

**Hypothesis (A) confirmed: central is privileged.** Every
eval drops; mean penalty -0.017 — uncannily identical to
exp 016's RC penalty (-0.017).

This rules out positional augmentation as a useful lever for
pELS. The cCRE midpoint contains the densest TF-binding/active
chromatin signal, and shifting the window introduces flanking
genomic content that dilutes the signal-to-noise.

**Compare 016 vs 017 — same penalty, different cause:**
| exp | trick                        | unique | mean  | Δ      |
|-----|------------------------------|--------|-------|--------|
| 012 | central, no augmentation     | 50K    | 0.758 |  base  |
| 016 | central + RC, half pool      | 25K    | 0.741 | -0.017 |
| 017 | random offset, full pool     | 50K    | 0.741 | -0.017 |

Two very different perturbations both cost -0.017 mean. This
suggests the model has a fairly tight tolerance around the
"centered cCRE midpoint, single strand, full pool" configuration.

**Eval-13 takes the smallest hit (-0.009).** eval_13 was the
"composition-helping" eval (exp 003), the only one where
flanking-genomic composition helps. Off-center windows include
more flanking, slightly counteracting the loss for this eval.

## Theory update

**New rule (positional):** central-200bp on cCRE midpoint is
privileged extraction. Off-center windows uniformly hurt.
Combined with the RC negative (016): both per-element
augmentations (transformation OR positional) cost the model
~-0.017.

**Augmentation playbook for cCREs is now empty.** Neither RC
nor positional variation helps. The pure-class central-window
recipe is optimal at the per-element level.

**Implication:** push performance must come from POOL-level
choices:
1. Better single-class selection (CA-CTCF, CA-H3K4me3, CA-TF
   not yet tested)
2. Quality filtering within a class (signal strength,
   conservation, cell-type breadth)
3. Cross-class subset selection (pick "best" cCREs across all
   classes by some quality criterion)
4. New eval_08-targeted designs (still need ~+0.10 here)

## Next experiment

**Exp 018: CA-CTCF only.** 126K-element pool (largest of the
remaining untested SCREEN classes). Completes the single-class
matrix for "accessibility-related" subtypes. CA-CTCF is
chromatin-accessible regions overlapping CTCF binding.
Insulator/boundary biology — distinct grammar from
enhancer-like pELS/dELS.
