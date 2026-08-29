# Experiment 018: CTCF ChIP-seq augmented library

## Design
- 15K cCRE (6K dELS + 4K pELS + 2K PLS + 1.5K CA_TF + 1.5K CTCF)
- 21K DNase (7K each cell)
- 9K CTCF ChIP-seq peaks (3K each cell, ENCFF519CXF / ENCFF543WTP / ENCFF540DWT)
- 5K random
Seed=18.

CTCF ChIP-seq has the strongest, most defined motif in the genome.

## Results — in noise band, no breakthrough
eval_01 = **0.0743** (K562=0.0775, HepG2=0.0786, SKNSH=0.0668)

| eval | 009 | 018 |
|---|---|---|
| 01 | 0.0772 | 0.0743 |
| 01 K562 | 0.0799 | 0.0775 |
| 01 HepG2 | 0.0812 | 0.0786 |
| 01 SKNSH | 0.0705 | 0.0668 |
| 13 | 0.1409 | 0.1432 |

CTCF ChIP did not help. Even the strongest motif source is in noise band.

## What I learned
**Adding qualitatively new signal types still hits the noise band.**
- DNase (009): in band
- DNase + H3K27ac (010): in band
- Multi-cell DNase (012): in band
- Top-signal DNase (014): in band
- cCRE-DNase intersection (017): in band
- CTCF ChIP-seq (018): in band

The model has a hard ceiling at eval_01 ~0.077 on this pipeline,
regardless of which "genomic regulatory" source we use.

## Theory: the noise band IS the answer
For this prepare.py pipeline, the optimal library is ANY mix of cCREs,
DNase peaks, and similar genomic regulatory sequences with a few percent
random. The compositional details within "genomic regulatory" are noise.

## Next: combine best signals into one "kitchen sink" design (019)
Last chance for a real breakthrough: combine 5 distinct signal types in
one library:
- 10K cCRE-DNase intersection
- 15K pure cCRE
- 15K DNase
- 5K CTCF ChIP
- 5K random
If still in noise band, conclude pipeline is saturated and start
replicating 009 to establish its true mean.
