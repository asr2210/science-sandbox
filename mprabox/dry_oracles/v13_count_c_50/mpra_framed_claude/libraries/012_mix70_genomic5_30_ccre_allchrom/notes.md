# Experiment 012 — 70/30 mix with cCREs from all chromosomes

## Results vs 70/30 with chr5 cCREs (009)
| eval | 009 (chr5 cCRE) | 012 (allchrom cCRE) | Δ |
|------|-----------------|---------------------|---|
| 01 ★ | **0.5748** | 0.5728 | -0.002 |
| 04 | **0.5695** | 0.5534 | -0.016 |
| 07 | 0.6069 | 0.6162 | +0.009 |
| 08 | 0.1560 | 0.1192 | -0.037 |
| 13 | 0.5897 | 0.5992 | +0.010 |
| mean8 | 0.581 | 0.565 | -0.016 |

## Verdict
Broadening the cCRE chromosome pool hurts slightly. The chr8/19/21/22/X
cCRE pool had higher GC (chr19, chr22 are GC-rich) which was helping. All
chromosome pool has more diversity but lower mean GC.

## Pattern: GC content of the supplemental source matters
Compositional alignment with the eval distribution remains the dominant
lever. Just adding "more diverse" cCREs without ensuring GC alignment
doesn't help.

## Implication
- Best library remains 009 (70/30 chr5 cCRE) at eval_01=0.5748.
- The cCRE supplement is partly about GC and partly about motif density.
- Pushing further needs a fundamentally different source — not more cCREs.
