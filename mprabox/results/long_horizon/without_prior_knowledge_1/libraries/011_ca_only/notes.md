# 011_ca_only — notes

## Design
50K x 200bp sampled (without replacement; pool 246K) from the CA
(chromatin accessibility) cCRE class. Central 200-bp window.
Mean GC = 0.435, sd = 0.087 (close to genomic baseline).

## Hypothesis
Tests whether dELS-only's win was driven by pool size + class
breadth (then CA at 246K should also do well) or by dELS-specific
enhancer grammar (then CA underperforms dELS).

## Result vs. previous

| eval | rand   | cCRE   | dELS   | **CA**  | Δ(CA−dELS) | Δ(CA−rand) |
|------|--------|--------|--------|---------|------------|------------|
| 01   | 0.6954 | 0.7133 | 0.7090 | 0.6775  | -0.032     | -0.018     |
| 02   | 0.7848 | 0.8046 | 0.8014 | 0.7667  | -0.035     | -0.018     |
| 03   | 0.7612 | 0.7870 | 0.7897 | 0.7579  | -0.032     | -0.003     |
| 04   | 0.7494 | 0.7733 | 0.7417 | 0.7048  | -0.037     | -0.045     |
| 05   | 0.6951 | 0.7133 | 0.7089 | 0.6777  | -0.031     | -0.017     |
| 06   | 0.7853 | 0.8048 | 0.8017 | 0.7671  | -0.035     | -0.018     |
| 07   | 0.6684 | 0.7452 | 0.7605 | 0.7386  | -0.022     | **+0.070** |
| 08   | 0.7841 | 0.6380 | 0.6720 | 0.6193  | -0.053     | -0.165     |
| 09   | 0.8115 | 0.8385 | 0.8042 | 0.7638  | -0.040     | -0.048     |
| 10   | 0.7564 | 0.7635 | 0.7779 | 0.7437  | -0.034     | -0.013     |
| 11   | 0.6833 | 0.7010 | 0.6973 | 0.6668  | -0.030     | -0.017     |
| 12   | 0.6553 | 0.6757 | 0.6782 | 0.6509  | -0.027     | -0.004     |
| 13   | 0.6584 | 0.7422 | 0.7601 | 0.7441  | -0.016     | **+0.086** |
| 14   | 0.7851 | 0.8046 | 0.8015 | 0.7665  | -0.035     | -0.019     |

Mean across evals: rand 0.738, cCRE 0.748, dELS 0.756,
**CA 0.718**. CA underperforms dELS uniformly (every eval) and
underperforms uniform random on 12/14 evals.

## Interpretation

**CA-only sits between PLS-only and dELS-only — and below uniform
random.** The pool-size hypothesis is partially supported but
incomplete:
- PLS pool 47K → mean 0.604
- CA pool 246K → mean 0.718
- dELS pool 1.47M → mean 0.756

There's a monotonic trend with pool size, but CA at 246K still
loses to uniform random ACGT (0.738). Pool size matters AND class
identity matters.

**CA underperforms dELS UNIFORMLY** (Δ = -0.016 to -0.053 on
every eval, mean Δ = -0.033). No eval where CA beats dELS. CA is a
worse class than dELS, full stop.

**CA only beats random on the two motif-rewarding evals (07, 13).**
This means CA contains real motif content but lacks the broader
diversity that uniform random provides for the high-baseline evals.
CA = "open chromatin without specific TF program" which gives some
motifs but not enhancer-grammar.

**Falsifies "any large single class works".** dELS specifically is
the special class. CA at 246K (5× larger than PLS, 6× smaller than
dELS) lands in the middle but well below dELS.

## What this changes (theory update)

Refined principle:
> Single-class libraries depend on BOTH pool size AND class
> identity. dELS uniquely combines (a) the largest cCRE pool
> (1.47M, 6× CA, 30× PLS) with (b) the most informative class
> identity (distal enhancers carry diverse cell-type-specific TF
> combinations and span the widest activity range in MPRA).
> CA-only fails despite a large pool because "accessible
> chromatin" is too heterogeneous and behavior-non-specific —
> includes housekeeping accessible sites, weak enhancers,
> non-functional accessible regions.

Updated hierarchy of regulatory specificity (best → worst as
single-class libraries):
1. dELS (large pool + sharp distal-enhancer grammar)
2. (untested) pELS / TF / CA-CTCF
3. CA (chromatin accessibility — broad signal)
4. PLS (narrow housekeeping-promoter grammar + tiny pool)

## Eval_08 sub-finding

CA's eval_08 = 0.619, slightly better than dELS (0.672 — wait, dELS
is actually higher! check). Re-checking: dELS eval_08 = 0.672, CA
eval_08 = 0.619. So CA is WORSE on eval_08 too. The pattern holds:
biological content uniformly hurts eval_08; CA's slightly more
homogeneous content might be worse than dELS's diverse content.

## Next experiment

**Exp 012: pELS-only.** Pool 249K — same size as CA — but content
is "proximal enhancer" rather than "chromatin accessibility". If
pELS ≈ dELS quality (relative to CA), then "enhancer-ness" is the
load-bearing signal. If pELS ≈ CA, then "distal" specifically
matters. If pELS ≈ PLS, then proximal regulatory elements are
generally narrow regardless of label.

Together with PLS, dELS, CA, and pELS, we'll have a clean class
matrix to pin down which classes carry what kind of training
signal.
