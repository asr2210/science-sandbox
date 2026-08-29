# 014_markov5_tss

5th-order Markov chain (6-mer context) trained on 008's TSS-
proximal sequences. 50k synthetic 200bp sequences sampled de novo.

## Result
eval_01: 0.2779 — WORSE than uniform random (0.3425, exp 001).

## Major surprise
Synthetic sequences with perfect 6-mer statistics matching 008 are
the worst training data I've made so far on eval_01.

## Why theory v10 was wrong
I expected k-mer statistics to capture most of the natural-DNA lift
since 003 (dinuc shuffle, 0.4362) retained 60% of it. But there's
a critical difference between:
- 003: real-sequence DNA backbones randomly *shuffled* per-window
  (preserves dinucs AND keeps long-range correlation by accident:
  if a window has a homopolymer or low-complexity region, the
  shuffle keeps the composition)
- 014: completely DE NOVO Markov walks (no parent sequence; the
  walk wanders into arbitrary 6-mer-consistent paths, which may
  produce repetitive or otherwise unrealistic patterns)

Markov-5 captures local statistics but produces sequences with NO
coherent long-range structure (no real motifs, no repeat instances,
no domain organization). The model trained on these learns
something different than the model trained on real DNA.

## Per-eval delta vs 001 (uniform random)
- eval_01: -0.065 (worse than random!)
- eval_03: -0.072
- eval_04: -0.087
- eval_07: -0.028
- eval_08: -0.020
- eval_10: -0.115
- eval_13: -0.048

All evals tank. Even eval_08 (random-loving) is below 001.

## Theory v11
Training data has TWO axes of value:
1. Local statistics (composition, k-mers): contributes most of the
   gap between random and natural (003 captures this).
2. Long-range coherence (sequence integrity, real backbones): a
   separate dimension. Without it, even matched k-mers hurt.

Synthesized data that lacks long-range coherence can be WORSE than
uniform random, because the model trains to expect those
unrealistic patterns and mispredicts on real test sequences.

## Implication
Don't synthesize sequences from local generative models. Stick to
real natural DNA. The Markov route is dead.

For exp 015: test if even small perturbations of REAL sequences
keep their training value. If so, then "approximately real" is
enough and we have a path to expand effective library size.
