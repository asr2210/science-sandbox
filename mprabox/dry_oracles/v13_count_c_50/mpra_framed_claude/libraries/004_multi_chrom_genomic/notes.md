# Experiment 004 — Multi-chromosome random genomic

## Design
10,000 random 200bp windows from each of chr8, chr19, chr21, chr22, chrX
(50,000 total). Sampled with rejection of any non-ACGT base. Shuffled.

## Results vs prior libraries
| eval | rand | chr19 | 50/50 | multi-chr (this) |
|------|------|-------|-------|------------------|
| 01 ★ | 0.129 | 0.526 | 0.433 | **0.555** |
| 02 | 0.128 | 0.527 | 0.434 | 0.556 |
| 03 | 0.077 | 0.514 | 0.411 | **0.560** |
| 04 | 0.390 | 0.585 | 0.533 | 0.509 |
| 06 | 0.119 | 0.523 | 0.424 | 0.555 |
| 07 | -0.142 | 0.490 | 0.325 | **0.628** |
| 08 | **0.580** | 0.292 | 0.412 | **0.021** ❌ |
| 10 | 0.094 | 0.441 | 0.331 | 0.501 |
| 13 | -0.147 | 0.479 | 0.310 | **0.614** |
| mean8 | 0.13 | 0.485 | 0.398 | 0.500 |

## Key findings
1. **Multi-chromosome wins eval_01 and eval_07/13.** Big jumps on eval_07
   (+0.14) and eval_13 (+0.13). These evals reward broader genomic
   distribution.
2. **eval_08 collapsed (0.29 → 0.02).** chr19 is GC-rich; broader genome
   has lower average GC. eval_08 prefers high-GC or random-like content.
3. **eval_04 slightly down (0.585 → 0.509)** — interesting. Not all evals
   benefit equally from genomic diversity.
4. Runtime keeps dropping (10s eval, 40s total). Pipeline is fast.

## eval_08 hypothesis
eval_08's targets are probably enriched for GC content. Random sequences
have GC ≈ 50%; chr19 has GC ≈ 48%; whole genome ≈ 41%. eval_08 scores in
order: random (0.58) > chr19 (0.29) > multi-chrom (0.02). Confirms.

## Theory update
- Diversity within "natural" matters, but composition (GC) is a real lever.
- eval_08 is a single eval and the multi-chrom hit on it costs ~0.27 there.
  Still, mean across 8 unique evals went from 0.485 → 0.500, so it's a net
  win.
- The path forward: keep grammar diversity, find a way to handle eval_08
  separately (perhaps via GC-stratified sampling).
