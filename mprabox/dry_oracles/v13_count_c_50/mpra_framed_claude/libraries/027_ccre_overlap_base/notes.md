# Experiment 027 — cCRE-overlap base library

## Design
35k mc5 random 200bp windows REQUIRED to overlap any cCRE annotation +
15k type-balanced cCRE supplement. Idea: enrich motif density in base
while keeping random window positions.

## Result vs 013
| eval | 013 | 027 (cCRE-overlap base) | Δ |
|------|-----|--------------------------|---|
| 01 ★ | **0.5765** | 0.5092 | -0.067 |
| 04 | 0.5774 | **0.5954** | +0.018 |
| 07 | **0.6037** | 0.4378 | -0.166 |
| 08 | 0.1730 | **0.3721** | **+0.200** |
| 10 | **0.5087** | 0.4253 | -0.083 |
| 13 | **0.5865** | 0.4119 | -0.175 |

Base GC: 0.487 (vs mc5 random 0.42). Library GC: 0.499 vs 0.460.

## What went wrong: motif enrichment is FUSED with composition shift
Requiring base windows to overlap cCREs implicitly biases the base
toward HIGH-GC regions (cCREs are GC-rich). The base lost its low-GC
component, eval_07/13 crashed. eval_08 hit an all-time high of 0.37
because the library is now extremely composition-shifted.

So I cannot enrich motifs in the base without also shifting composition;
the two are entangled in the genome.

## Theory v20
The mc5 base's value is DUAL:
1. Provides REAL MOTIF GRAMMAR (real cis-regulatory sequence)
2. Provides the LOW-GC distribution that balances the supplement's
   high-GC content

By replacing mc5 with cCRE-overlap mc5, I removed (2). The high-GC
shift dominated and broke eval_07/13.

This explains why 013 sits at the eval_01 maximum: the mc5 base provides
the LOW-GC reference distribution + real motif grammar, the cCRE
supplement provides the high-GC compositional shift. Together they
form a wide, multi-modal distribution that covers the eval well.

## Implication
Cannot enrich motifs in the base via cCRE-overlap without breaking
composition. To test motif-only-enrichment cleanly, would need to
SUBSAMPLE cCRE-overlap windows to match mc5 GC distribution — that
decouples motif density from GC.
