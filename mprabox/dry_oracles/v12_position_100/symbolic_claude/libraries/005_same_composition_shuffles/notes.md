# Exp 005: Same-composition shuffles

## Setup
50K sequences. Each sequence has exactly 50 each of {0,1,2,3}.
Permutation/order varies; composition does NOT.

## Results
All evals ≈ 0 (range -0.02 to +0.005). NOISE FLOOR.

## Theory update — KEY FINDING
Random library: mean_r ≈ 0.06
Same-composition shuffles: mean_r ≈ 0

**Almost all of the random baseline signal comes from COMPOSITION VARIANCE across sequences**, not from positional/motif content within sequences.

This dramatically narrows my search. To beat random, I should AMPLIFY across-sequence compositional variance. Per-sequence ordering matters very little.

## Sub-observation
Condition_c tends to be near 0 while condition_a, b are slightly negative.
Possibly conditions use different feature aggregations; condition_c may be slightly more order-sensitive.

## Next plan
- Exp 006: Dirichlet-extreme compositions. Each seq draws character weights from Dir(0.3,0.3,0.3,0.3) → highly biased per seq.
- Exp 007: Bimodal compositions (some seqs 80% '0', others 80% '3', etc.)
- Exp 008: Maximize compositional spread by deterministic blocks
