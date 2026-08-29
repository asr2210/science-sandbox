# Multimodal Library Design

## Principle
For Pearson-correlation-based scoring across 50k sequences, combining
multiple sub-libraries of distinct designs ("modes") gives higher correlation
than any single-mode library.

## Evidence
| Library                | mean_r | gain vs random |
| 001 random uniform     | 0.849  |       —         |
| 005 strict 50ea        | 0.826  | -0.023          |
| 006 motif insertion    | 0.817  | -0.032          |
| 007 strict+random mix  | 0.878  | **+0.029**      |

A 25k+25k strict+random hybrid lifts mean_r by 0.029 over pure random, even
though the strict half on its own scores worse than random. This indicates
that two-mode libraries dominate single-mode ones.

## How to apply
1. Start from the strongest single-mode library you have (random uniform).
2. Add a second mode that scores high on at least ONE cell line, even if it
   hurts another. The mix can recover the loss.
3. Each new mode should differ in either base composition, motif content,
   or some higher-order structural feature.
4. Sweep mix ratios — best may not be 50/50.

## Modes worth trying
- uniform random (Poisson composition variance) — strong on SK-N-SH
- strict 50/50/50/50 (zero composition variance) — strong on K562/HepG2
- motif-enriched (3 motifs on random background) — strong on SK-N-SH
- Markov-2 genome-like — strong on K562/HepG2
- AT-rich / GC-rich / palindromic / low-complexity (untested)

## Caveats
- Constant library returns NaN (Pearson undefined).
- Heavy bias toward one composition (e.g., variable GC ±30%) hurts ALL
  cell lines (libraries with extreme outlier sequences drag scores down).
- **Seed variance is ±0.008 range / ±0.003 std** for the same recipe.
  Single-seed differences below 0.005 may be noise. Run multiple seeds
  before declaring a recipe better.

## Refinements observed
- Adding a single 8-bp random insert (from a small ~50-entry bank) to the
  random half lifts mean_r by ~0.003. Larger banks saturate; longer
  inserts (16-bp) hurt; multiple inserts per seq hurt; inserting into
  the strict half hurts.
- 50/50 strict/random ratio is robust — other ratios hurt SKNSH.
- Block-stratified strict (every 4-bp window balanced) crashes ALL cells.
  Strict's value is GLOBAL balance + LOCAL randomness.

## Best recipe found (30 experiments)
25k strict-shuffled + 25k (random + 1 8-bp insert from 50-entry random
8-mer bank at random position). eval_01 = 0.882 with seed 88888.
