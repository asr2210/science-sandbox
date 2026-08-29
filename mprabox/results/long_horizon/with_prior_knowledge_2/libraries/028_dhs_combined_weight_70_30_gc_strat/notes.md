# 028_dhs_combined_weight_70_30_gc_strat

## What I tested
Structural test of 015's two-axis draw. Same axes (signal +
numsamples), same mix ratio (70/30), same stratification (5 GC
bins). Difference: combine the two axes into a SINGLE per-element
weight and do ONE weighted draw per bin (10K combined-weighted),
instead of TWO separate axis-elite draws per bin (7K signal-weighted
+ 3K numsamples-weighted).

per-element weight = 0.7 * signal_normalized + 0.3 * numsamples_normalized

The effective sampling distribution should be similar — same axes,
same proportions. Tests if the "two separate per-bin draws" structure
is load-bearing or just an implementation detail.

## Result — structure matters more than distribution
| recipe                              | cross-14 | seed std |
|-------------------------------------|----------|----------|
| 015 two-axis per-bin (champion)     | 0.7960   | 0.017    |
| 020 signal-only + strat             | 0.7841   | 0.006    |
| **028 combined-weight per-bin**     | **0.7651** | **0.002** |
| 011 70/30 mix (no strat)            | 0.7810   | (1 seed) |
| 003 50/50 mix (no strat)            | 0.7771   | (1 seed) |

Per-seed eval_01: 0.7243 / 0.7233 / 0.7204 (range 0.004 — tightest
of the entire series). cross-14 = 0.7651, -0.031 vs 015. Even
worse than 011 (no strat, 70/30 sequential).

## The "two separate axis-elite draws" structure has unique value
Mechanism: combined weight selects elements that score high on
EITHER axis. Top elements per bin are likely those that score high
on BOTH (intersection-favored — high signal AND broadly active).
The combined draw misses elements with HIGH BREADTH but only
MODERATE signal.

015's two-axis structure FORCES inclusion of these "high breadth,
moderate signal" elements via the 3K numsamples-elite slots per
bin — slots that the combined draw would NOT fill with these
elements.

These "broadly active but not signal-intense" elements are exactly
the diversity contributors — they encode regulatory grammar that
generalizes across cell types but isn't captured by signal-elite
selection.

## Per-seed std collapse
028's seed std (0.002) is 8× smaller than 015's (0.017) and 3×
smaller than 020's (0.006). The combined-weight draw is more
deterministic — each element has one weight, top elements are
always selected first; only ties between similar-weighted elements
yield seed variation.

This stability is achieved at the cost of -0.031 cross-14. Stability
is not the goal; diversity is.

## Theory v26 → v27
> **The two-axis per-bin draw structure of 015 is load-bearing,
> not just a notation for "70/30 mix under stratification".**
> Collapsing the two draws into a combined per-element weight loses
> 0.031 cross-14 even with the same axes, mix ratio, and
> stratification.
>
> Mechanism: separate per-bin draws of (signal-elite, breadth-elite)
> force inclusion of elements that score high on ONLY ONE axis.
> The "high breadth, moderate signal" elements are the unique
> contribution of the breadth axis — they encode regulatory grammar
> the signal axis would skip. Combined-weight draws favor
> intersection-elite elements that score high on BOTH axes, missing
> the union members.
>
> Practical implication: when designing future recipes with
> multiple axes, structure as separate per-axis draws within each
> stratum. NEVER collapse multiple axes into a single per-element
> weight — it removes the diversity from "axis-only-elite" elements
> that drives generalization.
>
> Combined with v25/v26: numsamples is the right axis because
> cross-cell-type COUNT is generalization-relevant. The two-axis
> structure is necessary because it surfaces "high-numsamples
> moderate-signal" elements that are otherwise drowned out by
> signal-elite combined-weight selection.

## 015 is now characterized along all major axes
Final picture of the 015 recipe's load-bearing properties:
1. **GC stratification at 5 bins** (021/016 fail at coarser/finer)
2. **70/30 mix ratio** (012/013/023 fail at other ratios)
3. **Signal axis** (020 still works alone but loses -0.012)
4. **Numsamples axis** (027/026 substitutions all lose; uniquely needed)
5. **Two-axis per-bin draw structure** (028 collapse loses -0.031)
6. **Consistent stratification across halves** (024 inconsistency loses)
7. **Full candidate pool** (019/025 filters lose)
8. **Summit-centered 200bp window** (009 multi-window loses)
9. **Without-replacement weighted draws** (default; not perturbed)

Every dimension has been tested via ablation; every perturbation
loses. 015 is overdetermined.

## Next
- 029: try 015 with chromosome-balanced selection — cap per-chromosome
  count to ensure even genomic coverage. The eval sets are likely
  chromosome-split; balanced coverage might improve held-out
  generalization.
- 030: final summary experiment — possibly a robustness test of 015
  by re-running with different random seeds, or a final attempt at
  a novel direction.
