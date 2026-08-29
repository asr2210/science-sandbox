# 003_dinuc_shuffled_ccre — notes

## Design
Same per-seed cCRE source sequences as exp 002, dinucleotide-preserving
shuffle applied to each sequence independently (Altschul-Erickson
algorithm). 13/50K sequences (0.026%) fell back to mononucleotide shuffle
because the arborescence search failed; aggregate dinucleotide deviation
over the whole library is 5e-6 (negligible). Mean GC = 0.47, sd = 0.11
(matches exp 002 by construction).

## Hypothesis
A clean disambiguation of composition vs motif content. Predicted:
- shuf cCRE > random  (composition contributes)
- shuf cCRE < cCRE    (motifs contribute)

## Result vs. previous baselines

| eval | rand   | cCRE   | shuf   | Δ(shuf−rand) | Δ(cCRE−shuf) |
|------|--------|--------|--------|--------------|--------------|
| 01   | 0.6954 | 0.7133 | 0.6500 | **-0.045**   | +0.063       |
| 02   | 0.7848 | 0.8046 | 0.7343 | -0.051       | +0.070       |
| 03   | 0.7612 | 0.7870 | 0.7169 | -0.044       | +0.070       |
| 04   | 0.7494 | 0.7733 | 0.6833 | -0.066       | +0.090       |
| 05   | 0.6951 | 0.7133 | 0.6498 | -0.045       | +0.064       |
| 06   | 0.7853 | 0.8048 | 0.7365 | -0.049       | +0.068       |
| 07   | 0.6684 | 0.7452 | 0.6675 | -0.001       | +0.078       |
| 08   | 0.7841 | 0.6380 | 0.6430 | -0.141       | -0.005       |
| 09   | 0.8115 | 0.8385 | 0.7392 | -0.072       | +0.099       |
| 10   | 0.7564 | 0.7635 | 0.7107 | -0.046       | +0.053       |
| 11   | 0.6833 | 0.7010 | 0.6408 | -0.043       | +0.060       |
| 12   | 0.6553 | 0.6757 | 0.6168 | -0.039       | +0.059       |
| 13   | 0.6584 | 0.7422 | 0.6880 | **+0.030**   | +0.054       |
| 14   | 0.7851 | 0.8046 | 0.7342 | -0.051       | +0.070       |

Mean across evals: rand 0.738, cCRE 0.748, shuf **0.687**.

## Interpretation

**Shuffled cCRE is WORSE than uniform random on every eval except 13.**
This is surprising and overturns my prior. Three things follow:

1. **The cCRE gain is overwhelmingly motif-driven, not composition-driven.**
   Where cCRE beats random by, say, +0.018 on eval_01, that gain comes
   from motif content — destroying motifs while preserving composition
   actually pushes performance BELOW random.
2. **Narrow composition is actively harmful.** cCRE composition is
   GC-biased and dinucleotide-non-uniform (CpG islands, repeat-masked
   regions, etc.). When you train on sequences locked to that narrow
   composition with no motif content, the model becomes overspecialized
   and generalizes worse than a model trained on uniform composition.
3. **Wide composition coverage is a feature, not a bug, of uniform
   random.** Random gives the model exposure to the full sequence
   space. cCRE-only adds motifs but narrows composition. The optimum
   is probably "wide composition AND motif content" — i.e., motifs in
   diverse backgrounds.

Per-eval breakdown:
- **eval_07: composition does nothing, motifs do everything.**
  random→shuf is essentially flat (0.668→0.668), shuf→cCRE is +0.078.
  This eval is purely motif-rewarding.
- **eval_13: composition contributes, motifs contribute more.**
  random→shuf +0.030, shuf→cCRE +0.054.
- **eval_08: rewards random-uniform composition; both biological
  composition AND motifs hurt.** Both shuf (0.643) and cCRE (0.638)
  are well below random (0.784).
- **All other evals: composition mildly hurts, motifs mildly help.**

Cell-type pattern: with shuffled-cCRE the SKNSH > K562 > HepG2 ordering
becomes much weaker — most evals have all three cell types within 0.01.
Suggests SKNSH's higher correlation depends on real motif content.

## What this changes (theory update)

Old theory: "biology probably helps because regulatory grammar
generalizes." → mostly correct in spirit but I was conflating
composition and motif syntax.

New theory: **The signal that generalizes across cell types is *motif
content*, not regulatory composition. Wide sequence-space coverage
(uniform composition) acts as a regularizer that helps the model
generalize. The ideal library has motifs embedded in compositionally
diverse backgrounds.**

This makes biological sense: TF binding preferences are largely shared
across cell types (the same TF binds the same motif everywhere it is
expressed). Composition (GC-biased CpG islands) is more cell-type
specific because it's tied to chromatin architecture.

## Next experiment

The most decisive next experiment: **motif-injected random library.**
Take uniform-random 200-bp backgrounds, inject 1–5 known TF binding
motifs (sampled from JASPAR or HOCOMOCO) at random positions in each.
This isolates "motifs in arbitrary backgrounds" from "motifs in
genomic context." If this matches or beats cCRE on the motif-rewarding
evals (07, 13), then motifs are sufficient — we don't need genomic
backgrounds. If it falls short, motif spacing/syntax/genomic flanking
also carries information.
