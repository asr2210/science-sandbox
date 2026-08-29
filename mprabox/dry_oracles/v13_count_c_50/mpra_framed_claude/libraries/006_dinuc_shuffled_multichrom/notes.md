# Experiment 006 — Dinucleotide-shuffled multi-chromosome genomic

## Design
Take exp 004's multi-chrom genomic sequences, dinucleotide-shuffle each
(Altschul-Erikson Eulerian algorithm). Preserves dinucleotide composition
exactly while destroying all motif structure. Same per-sequence k=2
k-mer distribution; randomized k≥3 structure.

## Diagnostic value
This isolates the contribution of motifs vs k-mer composition.

## Results — the killer comparison
| eval | random | dinuc-shuffled multi-chrom (this) | real multi-chrom (004) |
|------|--------|-----------------------------------|------------------------|
| 01 ★ | 0.129 | **0.445** | 0.555 |
| 02 | 0.128 | 0.445 | 0.556 |
| 03 | 0.077 | 0.450 | 0.560 |
| 04 | 0.390 | 0.320 | 0.509 |
| 06 | 0.119 | 0.445 | 0.555 |
| 07 | -0.142 | 0.550 | 0.628 |
| 08 | 0.580 | 0.066 | 0.021 |
| 10 | 0.094 | 0.469 | 0.501 |
| 13 | -0.147 | 0.538 | 0.614 |

## The breakdown of where performance comes from
On eval_01:
- random → dinuc-shuffled-natural: +0.316 (composition / k-mer effect)
- dinuc-shuffled → real-natural:    +0.110 (motif effect)

**~74% of the gain attributed to "natural sequences" comes from
dinucleotide composition. Only ~26% comes from real motif structure.**

## Theory v5 → v6: composition dominates over grammar
For the prepare.py model on this task:
- The dominant signal in the library is k-mer composition (GC content,
  dinucleotide frequencies). This explains the bulk of cross-eval variance.
- Motif grammar contributes a meaningful but smaller marginal gain
  (~0.1 on eval_01).
- This is consistent with: a relatively small model trained on 50k
  sequences cannot easily learn complex motif grammar — but can easily fit
  k-mer regression features.
- It also explains why curated (cCRE) libraries underperform random
  genomic: cCREs narrow the compositional distribution, costing more in
  compositional fit than they gain in motif clarity.

## Implications for library design
1. **Optimize compositional coverage first.** The library should span the
   compositional space the eval distribution occupies.
2. **Don't over-curate.** Curation narrows the compositional distribution.
3. **Diversity within natural sequences matters because it spreads
   compositions, not (mainly) because it spreads motifs.**
4. **There's still ~0.11 on the table from motif structure on eval_01.**
   To capture this, the library needs both compositional breadth AND
   real natural sequences (not just shuffled).

## Open: how high can compositional+motif diversity go?
- Best natural-only: 0.555 (multi-chrom, 5 chroms).
- More chromosomes → marginally more compositional diversity → marginal gain?
- Mixing shuffled + natural at right ratio → could it add k-mer coverage
  without losing motif signal? (mix-50 already hurt; need finer control.)
