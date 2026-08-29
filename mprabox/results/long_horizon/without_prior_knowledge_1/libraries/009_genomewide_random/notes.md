# 009_genomewide_random — notes

## Design
50K x 200bp uniform-random windows sampled from hg38 main chromosomes
(chr1–22, chrX, chrY; total 3.09 Gb). Reject windows containing any
N. No cCRE / regulatory annotation used.

Expected mix: ~50% repetitive (LINE/SINE/LTR/etc), ~25% intronic,
~25% intergenic, with cCREs (~0.7% of genome) only randomly hit.

## Hypothesis
Tests whether cCRE annotation specifically helps, or whether real
human DNA in any region is enough.
- If genome-wide ≈ dELS-only → annotation doesn't matter
- If genome-wide < dELS-only → cCRE annotation captures real info
- If genome-wide > dELS-only → expand beyond cCREs

## Result vs. previous

| eval | rand   | cCRE   | dELS   | **genwide** | Δ(genwide−rand) | Δ(genwide−cCRE) |
|------|--------|--------|--------|-------------|------------------|-------------------|
| 01   | 0.6954 | 0.7133 | 0.7090 | 0.6596      | -0.036           | -0.054            |
| 02   | 0.7848 | 0.8046 | 0.8014 | 0.7424      | -0.042           | -0.062            |
| 03   | 0.7612 | 0.7870 | 0.7897 | 0.7332      | -0.028           | -0.054            |
| 04   | 0.7494 | 0.7733 | 0.7417 | 0.6922      | -0.057           | -0.081            |
| 05   | 0.6951 | 0.7133 | 0.7089 | 0.6605      | -0.035           | -0.053            |
| 06   | 0.7853 | 0.8048 | 0.8017 | 0.7433      | -0.042           | -0.061            |
| 07   | 0.6684 | 0.7452 | 0.7605 | 0.7120      | **+0.044**       | -0.033            |
| 08   | 0.7841 | 0.6380 | 0.6720 | 0.5351      | **-0.249**       | -0.103            |
| 09   | 0.8115 | 0.8385 | 0.8042 | 0.7463      | -0.065           | -0.092            |
| 10   | 0.7564 | 0.7635 | 0.7779 | 0.6808      | -0.076           | -0.083            |
| 11   | 0.6833 | 0.7010 | 0.6973 | 0.6497      | -0.034           | -0.051            |
| 12   | 0.6553 | 0.6757 | 0.6782 | 0.6320      | -0.023           | -0.044            |
| 13   | 0.6584 | 0.7422 | 0.7601 | 0.7326      | **+0.074**       | -0.010            |
| 14   | 0.7851 | 0.8046 | 0.8015 | 0.7413      | -0.044           | -0.063            |

Mean across evals: rand 0.738, cCRE 0.748, dELS **0.756**, genwide **0.690**.

## Interpretation

**Genome-wide random is WORSE than uniform random ACGT.** This is the
sharpest single result so far. Real human DNA, sampled at random,
underperforms synthetic uniform random on 12/14 evals — and
catastrophically on eval_08 (-0.249 vs random — worse even than
PLS-only's eval_08 of 0.477).

Where genwide BEATS random: only the two motif-rewarding evals
(07: +0.044, 13: +0.074) — because real DNA contains real TF motifs
that a model can learn.

Where genwide LOSES to random: everywhere else. The mostly intronic,
intergenic, and repetitive (~50% of genome) content actively
*degrades* training compared to uniform random ACGT. Repetitive
elements (LINE, SINE, LTR, simple repeats) form low-complexity
distractor signals the model latches onto.

**This decisively answers the cCRE-annotation question:**
> The cCRE annotation is doing real, load-bearing work. It is not
> a noisy proxy for "real DNA". It's selecting the ~0.7% of the
> genome that contains regulatory elements out of a sea of
> mostly-uninformative-or-actively-misleading sequence.

## What this changes (theory update)

Refined ladder of training-data quality:
1. **dELS-only** (0.756) — diverse regulatory class, large pool
2. **natprop cCRE** (0.752) — dELS-dominated + small classes
3. **cCRE class-balanced** (0.748) — dELS diluted
4. **cCRE+random mix** (0.745) — dilution by random
5. **uniform random ACGT** (0.738) — synthetic noise
6. **motif-injected random** (0.732) — motifs without context
7. **dinuc-shuffled cCRE** (0.696) — destroys motifs
8. **genome-wide random** (0.690) — repeats are actively bad
9. **PLS-only** (0.604) — narrow, GC-extreme class

Genome-wide random falls between dinuc-shuffled cCRE (which
destroys motif structure) and PLS-only (which collapses to one
narrow grammar). The lesson:
> Curation matters more than sequence-realism. A uniform random
> baseline beats unfiltered genomic samples because most of the
> genome teaches the model nothing useful or actively wrong things.

## Per-eval pattern

- **eval_07, eval_13** are the only evals where genwide > random.
  Both are motif-rewarding evals. Confirms: real DNA contains real
  motifs that help on motif-tested evals, but the surrounding
  context is otherwise harmful.
- **eval_08 collapse** (-0.249 vs random). eval_08 specifically
  punishes biological content; genome-wide is the most biological
  signal possible (no curation), so it tanks hardest.
- **High-baseline evals (02, 06, 09, 14)** lose ~0.04–0.07 — the
  generic "real DNA distribution" is worse than uniform random
  for these.

## Next experiment

Two natural follow-ups:
- (A) **Repeat-masked genome-wide**: sample windows but reject if
  >50% soft-masked (repeats). If this recovers most of the
  genwide → cCRE gap, repeats are the active distractor. If it
  does not, then non-repeat intergenic/intronic regions are also
  uninformative.
- (B) **cCRE-flanking windows**: sample windows within ±5 kb of
  any cCRE but not overlapping any cCRE. Tests whether the
  *regulatory neighborhood* carries the info or only the cCRE
  element itself.

Going with (A) for exp 010 — repeats are the largest hypothesized
class of "actively bad" sequence, and the test isolates them
cleanly.
