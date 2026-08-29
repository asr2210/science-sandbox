# Experiment 016: Multi-window augmentation on 009 hybrid composition

## Design
6.7K unique regulatory loci × 3 shifted windows (offsets −100, 0, +100) +
5K random = 50K sequences. Composition mirrors 009.
- cCRE loci: 2.7K dELS + 1.7K pELS + 1K PLS + 0.7K CA_TF + 0.7K CA-CTCF = 6.8K × 3 = 20.4K seqs
- DNase loci: 2.7K × 3 cells × 3 windows = 24.3K seqs
- 5K random (single window)
Seed=16.

## Results — middle of noise band
eval_01 = **0.0751** (K562=0.0776, HepG2=0.0786, SKNSH=0.0690)

| eval | 009 | 016 |
|---|---|---|
| 01 | 0.0772 | 0.0751 |
| 02 | 0.0755 | 0.0736 |
| 06 | 0.0765 | 0.0753 |
| 08 | 0.0639 | 0.0642 |
| 10 | 0.1286 | 0.1278 |

All within the established noise band.

## What I learned
Multi-window augmentation did not break the band. Pattern is now
unambiguous: composition AND augmentation are both saturated. The model
on this pipeline has a hard ceiling around eval_01 ≈ 0.077.

Net effect of 3-window approach: trades source diversity (fewer unique
loci) for positional invariance (3 views per locus). Roughly equivalent
to single-window — suggests the model already learns positional invariance
sufficiently from single-window data.

## Theory update
**The bottleneck is model/pipeline, not library design.** Within "genomic
regulatory sequences" with reasonable composition, all designs perform
within ±0.004 of each other.

To find an improvement of practical interest, I either need:
- A qualitatively new signal type (TF ChIP-seq for strong motifs, etc.)
- OR multi-seed averaging to detect tiny but real effects
- OR confirm the plateau is real and stop chasing it

## Next
Try cCRE-DNase INTERSECTION — peaks confirmed by both signal types.
Highest-confidence regulatory regions. Tests label-confidence axis.
