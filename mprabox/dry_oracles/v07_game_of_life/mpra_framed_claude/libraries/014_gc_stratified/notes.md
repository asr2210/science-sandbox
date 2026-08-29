# Experiment 014 — GC-stratified pure natural

## Design
10K natural hg38 windows per GC bin (≤35%, 35-45%, 45-55%, 55-65%, >65%).
No regulatory enrichment. Just balanced composition.

## Result
- eval_01: **0.3939** (Δ +0.0063 vs nat baseline, MATCHES 4-way mix)
- K562: 0.6057, HepG2: 0.4300, SK-N-SH: 0.1460

## MAJOR theory update — T8
**The active lever behind regulatory enrichment is GC composition,
not motif content.** GC-stratified natural gives the same lift as
the 4-way regulatory mix:

| design | eval_01 | Δ vs nat |
|---|---|---|
| 4-way mix (60% reg) | 0.3937 | +0.0061 |
| **GC-stratified natural** | **0.3939** | **+0.0063** |
| max diversity | 0.3939 | +0.0063 |

Random hg38 windows (length-weighted) have GC distribution
centered at ~41%, heavily skewed toward AT-rich. cCRE/DHS regions
are enriched at CpG islands and high-GC promoters; when included
they shift the training distribution toward higher GC. The model
generalizes best when trained on broad GC representation, which
the natural genome under-samples in the high-GC tail.

## Implication for T7 retraction
T7 said "natural backbone + moderate reg." That's still true, but
the mechanism is GC, not motifs. Mix designs that include cCRE/DHS
work because they balance the GC distribution, not because they
provide regulatory grammar per se.

The 0.394 ceiling is the model's eval performance when training
data has broad GC coverage. Further library design must push GC
distribution to match what the eval expects, or pursue something
truly orthogonal (sequence augmentation, anti-repetitive masking,
etc).

## Next direction
Test orthogonality: combine GC stratification + regulatory mix.
If they're the same mechanism (GC), no further lift. If they're
orthogonal, lift may push 0.398+.
