# 002_encode_ccre_uniform

## Design
50,000 200bp windows centered on uniformly-sampled ENCODE V3 GRCh38
cCREs (~1.06M total: dELS, pELS, PLS, CTCF-only, DNase-H3K4me3).
cCREs are defined from chromatin features across hundreds of cell
types → broadly covers cross-cell-type regulatory grammar.

## Hypothesis
Real regulatory grammar lifts model performance over random.
Specifically: expected lift on HepG2 (random-blind cell type),
some lift on K562, expected lift on eval_08 (regulatory-grammar
diagnostic set).

## Result vs 001
                eval_01  K562    HepG2   SKNSH   eval_08
001 random:     0.2307   0.139   -0.089  0.642   0.089
002 cCRE:       0.3154   0.145   +0.177  0.625   0.076
delta:          +0.085   +0.006  +0.266  -0.017  -0.013

## What happened
HepG2 jumped from -0.09 to +0.18 (+0.27). This is the dominant
contribution to the eval_01 lift. HepG2 responds strongly to real
regulatory grammar that random sequences can't supply.

K562 essentially unchanged. r=0.14 → 0.15. Either:
(a) the cCRE pool is biased away from K562-active elements, so the
    model doesn't see enough K562-on signal to learn K562 grammar; or
(b) K562 activity has a hard ceiling around r=0.14 given this library
    size and architecture (intrinsic noise / measurement issue); or
(c) K562 grammar requires specific motifs that are rare in generic
    cCREs.

SK-N-SH dropped slightly (0.64 → 0.62). Random's compositional signal
was slightly better than cCREs for SK-N-SH. This is consistent with
SK-N-SH being a composition-driven cell type.

eval_08 went DOWN slightly (0.089 → 0.076). My earlier guess that
eval_08 measures regulatory-grammar separability is at least partly
wrong. eval_08 may instead measure something where compositional
diversity is more useful than cCRE-skewed sequences (e.g., wide
GC-range coverage, designed contrasts, non-natural-genome
sequences).

## Theory update
T1 → T2:
- Cell-type predictability profile: SK-N-SH is composition-rich, HepG2
  is grammar-rich, K562 is hard (composition gives baseline, cCRE
  doesn't add).
- The lift from cCREs comes almost entirely from HepG2, not the others.
- eval_08 is not measuring what I thought. May be diagnostic of NON-
  natural-genome features (synthetic, shuffled, motif-only).
- Broad cCRE sampling is a solid baseline (mean_r 0.32) but is missing
  the K562 lever and may be losing the eval_08 axis.

## Next experiment ideas
- Sample cCREs annotated as active in K562 specifically → test (a)
- Add dinucleotide-shuffled controls 50/50 → test motif/composition
  separability, hopefully lifts eval_08 and K562
- Stratify cCRE classes (PLS, pELS, dELS, CTCF-only) equally → test
  whether class skew matters
- Sample TF ChIP-seq peaks → stronger motif signal per sequence
- Tile fewer regions (Sharpr-style) → position