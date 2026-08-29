# 004_jaspar_motifs_planted

## Setup
50k uniform random 200bp backbones. Each has K∈{2,3,4} TF motifs planted at
random non-overlapping positions. Motifs are sampled from each of 879
vertebrate JASPAR 2024 PWMs (uniform over motifs, sample per-column from PWM).

## Result
- eval_01=0.4615 (LOWER than random 0.5131!)
- eval_07=0.6046, eval_13=0.5818 (motifs help these somewhat)
- eval_04=eval_09=0.2155 (CRASHED from 0.42 random, 0.60 cCREs)
- eval_08=0.1045 (worst yet)
- K562 r consistently > HepG2/SKNSH r (e.g., 0.52 vs 0.40 on eval_01)

## What this reveals
- Pure motif planting in random backbones is *worse* than pure random for
  most evals. Motifs don't carry meaning without realistic context.
- The K562 bias is striking: synthetic motifs preferentially help K562
  predictions. This suggests JASPAR motifs are well-curated for blood TFs
  (GATA1, KLF1, etc.) and underrepresent neural / hepatic TFs.
- eval_04/09 crashed: those evals appear to need *low-activity* prediction,
  and a motif-rich library teaches "predict high".
- eval_07/13 modestly improved: these reward strong-motif sequences.

## Theory update
There are at least two distinct types of evals:
1. **Motif/grammar-dominated** (eval_07, 13, partly 01): reward libraries
   that teach the model strong TF binding sites.
2. **Composition/baseline-dominated** (eval_04, 09, 08): reward libraries
   that teach the model what *non-active* sequences look like, so it
   doesn't overpredict.

Real cCREs are good for type 1 because they have motifs, and *okay* for
type 2 because they have natural composition. Synthetic motif-planting is
great for type 1 but bad for type 2.

## Implication for next steps
Stop trying synthetic-only libraries. Push the cCRE library further by
exploiting things that *natural cCREs already have* but my current library
might not maximize: positional context, strand symmetry, biosample diversity,
non-redundant element selection.
