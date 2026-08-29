# MPRA library design — empirical observations

What I learned from experiments 001–009 in this run. All numbers
refer to eval_01 from prepare.py on the same 50k×200bp library.

## Performance plateau on this benchmark

| design | eval_01 | notes |
|---|---|---|
| pure random iid ACGT | 0.116 | baseline floor (uniform composition) |
| random bg + 2-3 motifs | 0.124 | +0.008 |
| chr22 random 200bp windows | **0.134** | natural composition + motifs |
| chr22 dinuc-shuffled (motifs destroyed) | **0.133** | composition alone! |
| chr19+chr22 random | 0.133 | multi-chr no help |
| chr22 random + 2 motifs | 0.135 | augmentation barely helps |
| chr22 cCRE-centered | 0.126 | enrichment HURTS |
| 2500 seeds × 20 satmut | 0.098 | huge drop, narrow contexts |
| 25k random + 25k +motifs mix | 0.135 | same as either alone |

## Key principles (REWRITTEN after exp 009)

### THE BIG FINDING
**Dinucleotide composition alone explains the entire genomic
advantage** (random ACGT 0.116 → chr22 random 0.134 → chr22
dinuc-shuffled 0.133, same as chr22 random within noise).

At this scale (50k × 200bp, small CNN), the model is essentially
learning a "this looks compositionally like X → activity" mapping.
It does NOT learn motif syntax. Motif insertion gives ~0 lift.

### Principles
1. **Context diversity dominates.** 50,000 unique contexts beats
   2,500 contexts × 20 variants, badly.
2. **Composition is the actionable signal.** Dinucleotide
   distribution matches natural genome → eval performance ~0.134.
3. **Motif content is invisible** at this scale — adding/removing
   motifs has no measurable effect.
4. **Narrowing to CRE classes hurts** because cCREs have different
   composition (more GC-rich) than the eval distribution.

## Eval structure observed
14 evals, but only ~7 distinct: 01==14, 02==05, 03==12, 04==09,
06==11. eval_08 always lowest (~0.06 random, ~0.02 satmut).
eval_07 gives high K562 when GC-rich content present.

## Promising directions to try
- GC-rich vs GC-poor chr22 windows (does composition direction matter?)
- Promoter-region sequences (very high GC)
- Synthetic sequences with controlled GC/dinucleotide composition
- Mix multiple compositional regimes (broad compositional coverage)
- Massively augmented (RC) library to test data-doubling effects

## Failed directions
- Saturation mutagenesis (any form) — too few unique contexts
- cCRE-only enrichment — wrong composition
- Multi-chromosome random — no extra info
