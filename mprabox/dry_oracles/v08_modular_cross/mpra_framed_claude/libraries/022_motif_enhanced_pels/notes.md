# Experiment 022 — Motif-enhanced pELS backbone

## What I tested
35k pELS sequences with 10-20 motifs inserted into the real backbone
+ 15k pure pELS. Tests: does real genomic backbone + explicit motifs
beat random ACGT backbone + motifs?

## Result — eval_13 RECORD, mean lower
- **eval_13: mean=0.0067, K562=0.0120, SKNSH=0.0070** — RECORD on
  eval_13 mean (vs 018's 0.0054) and first time consistently positive
  across all 3 cell types.
- eval_10: 0.0030 (decent)
- eval_07: 0.0006 (lost)
- eval_08: -0.0027 (lost — backbone disrupted the pELS signal)
- Most other evals ≈ 0.0015 (half of pure motifs' 0.0034)
- Mean across 14 ≈ 0.0014

## What this tells me
**Real backbone + motifs is a new grammar** that unlocks eval_13.
But it disrupts BOTH:
- The pELS-natural signal that helped eval_07/08 (motifs disrupted it)
- The motif co-occurrence pattern that helped broad evals (real
  backbone has skewed k-mer distribution)

Net: lower mean, but eval_13 gained.

## Updates to theory
**v3.13 → v3.14:** Different "grammars" each have a specific eval
sensitivity:
- pure motifs (021) → broad evals
- low-density motifs + pELS (012) → eval_07/08
- high-density motifs + pELS (018) → eval_07
- low-density motifs + dELS (013) → eval_10
- motif-enhanced pELS (022) → eval_13

Each unique recipe = one new eval unlock. But each costs ~half on
the other evals.

## Next
Try CTCF-bound pELS specifically (more conserved/active subset of
pELS). Hypothesis: filtering to higher-confidence real elements
may give cleaner per-element signal.
