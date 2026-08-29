# 006_pls_only — notes

## Design
50K x 200bp sampled with replacement from the 47,532 ENCODE PLS
(promoter-like signature) cCREs. Central 200-bp window from GRCh38.
PLS GC content = 0.606 (CpG-island-rich, much higher than
class-balanced cCRE's 0.472 or random's 0.500).

## Hypothesis
PLS is the most regulatorily-dense element class — promoters carry
many TF binding sites for ubiquitously expressed factors. If element
class matters, PLS-only should match or beat class-balanced cCRE on
the motif-rewarding evals (07, 13).

## Result vs. previous

| eval | rand   | cCRE   | mix    | **PLS** | Δ(PLS-cCRE) | Δ(PLS-rand) |
|------|--------|--------|--------|---------|-------------|-------------|
| 01   | 0.6954 | 0.7133 | 0.6951 | 0.5903  | -0.123      | -0.105      |
| 02   | 0.7848 | 0.8046 | 0.7860 | 0.6657  | -0.139      | -0.119      |
| 03   | 0.7612 | 0.7870 | 0.7668 | 0.6278  | -0.159      | -0.133      |
| 04   | 0.7494 | 0.7733 | 0.7461 | 0.7022  | -0.071      | -0.047      |
| 05   | 0.6951 | 0.7133 | 0.6952 | 0.5901  | -0.123      | -0.105      |
| 06   | 0.7853 | 0.8048 | 0.7861 | 0.6655  | -0.139      | -0.120      |
| 07   | 0.6684 | 0.7452 | 0.7026 | 0.5091  | **-0.236**  | **-0.159**  |
| 08   | 0.7841 | 0.6380 | 0.6872 | 0.4774  | -0.161      | -0.307      |
| 09   | 0.8115 | 0.8385 | 0.8077 | 0.7543  | -0.084      | -0.057      |
| 10   | 0.7564 | 0.7635 | 0.7399 | 0.5925  | -0.171      | -0.164      |
| 11   | 0.6833 | 0.7010 | 0.6827 | 0.5789  | -0.122      | -0.104      |
| 12   | 0.6553 | 0.6757 | 0.6590 | 0.5372  | -0.139      | -0.118      |
| 13   | 0.6584 | 0.7422 | 0.6999 | 0.4912  | **-0.251**  | **-0.167**  |
| 14   | 0.7851 | 0.8046 | 0.7859 | 0.6661  | -0.139      | -0.119      |

Mean across evals: rand 0.738, cCRE 0.748, mix 0.738, **PLS-only 0.604**.

## Interpretation

**Catastrophic collapse.** PLS-only is dramatically worse on every
single eval — including the motif-rewarding ones I expected to win
on. eval_07 went from cCRE 0.745 to PLS 0.509 (below random's 0.668).
eval_13 from 0.742 to 0.491.

**Class diversity is huge.** A library restricted to a single
regulatory element class — even the most regulatorily-dense one
(promoters) — loses on every eval, including evals biased toward
biology.

Possible mechanisms:
1. **Narrow regulatory grammar.** PLS sequences contain only
   promoter motifs (TATA, INR, SP1, TBP). The eval test sequences
   include enhancer / CTCF / etc. content the model never saw.
2. **Extreme composition narrowness.** PLS GC = 0.606, sd = 0.123
   — far from uniform. The model overfits to CpG-island-style
   sequences and generalizes poorly to anything else.
3. **Activity range compression.** Promoters in MPRA may give
   uniformly high activity (saturated reporters), reducing the
   gradient signal for training.

The cell-type ordering is preserved (SKNSH > K562 ≈ HepG2 in nearly
every eval), confirming again that this is an assay-level effect.

## What this changes (theory update)

> Library diversity across regulatory element classes is critical.
> A library that restricts to one class — even the most
> regulatorily-dense one — fails to generalize. The model needs
> exposure to multiple kinds of regulatory grammar (promoter,
> enhancer, insulator, accessible chromatin) to learn features
> that transfer across the eval distribution.

This is consistent with the broader theory that wide composition
and motif diversity both matter. PLS-only is simultaneously narrow
in BOTH composition (high GC) AND motif content (only promoter
TFs). It fails on both axes.

The class-balanced cCRE design (exp 002) succeeded precisely
because it spread sampling across 8 element classes, giving wide
composition AND diverse motif syntax.

## Next experiment

Two strong candidates:
1. **dELS-only library.** Largest class (1.47M cCREs), distal
   enhancers, lower GC than PLS. If dELS also fails → all
   single-class libraries are bad and diversity is essential.
   If dELS does ok → there's something specific about PLS that
   broke it.
2. **Class-balanced cCRE + STARR-seq active filtering.** Restrict
   to cCREs measured to be active in MPRA-style assays. This
   enriches for sequences with strong activity gradients without
   sacrificing class diversity.

Going with (1) — dELS-only — first because it's the cleanest
diagnostic on the class-diversity question. Cheap and decisive.
