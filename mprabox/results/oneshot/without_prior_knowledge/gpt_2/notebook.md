# Lab notebook

## Initial interpretation

The goal is not to maximize activity in K562, HepG2, or SK-N-SH specifically.
The goal is to choose 50,000 200 bp DNA sequences that would be unusually
informative for learning general regulatory grammar from MPRA measurements.
Because the evaluation sets are anonymous and the assay is one-shot, I should
avoid narrow tissue-specific assumptions and instead cover broad classes of
sequence variation that a regulatory model ought to understand.

My working theory is that a good compact MPRA training library should combine:

- Natural enhancer-like and promoter-like sequence statistics, because real
  regulatory syntax includes motif density, spacing, local GC structure,
  repetitive sequence, CpG content, and weak motif clusters that synthetic
  random sequence will miss.
- Designed motif perturbation series, because models learn grammar fastest
  when the library contains controlled contrasts: motif present versus absent,
  orientation changes, spacing changes, copy-number changes, and background
  changes.
- Negative and near-negative backgrounds, because activity prediction requires
  learning what is not regulatory, not only recognizing strong functional
  elements.
- Wide sequence diversity, because the objective rewards training performance
  per sequence rather than saturating one family of elements.

I will not inspect `prepare.py`, per the instructions. I will use the final
black-box run only once after generating the library.

## Candidate sequence sources

Real genomic data would be attractive, especially accessible chromatin peaks,
enhancers, promoters, lncRNA/intronic regions, shuffled controls, and
phylogenetically conserved elements. However, downloading and curating large
genome annotations creates risk: coordinate mismatch, hidden duplicates,
ambiguous bases, and a library biased toward the few source tissues or assays I
choose. Because this run is one-shot and the current workspace has no bundled
reference data, I favor a self-contained generator with explicit sequence
classes that approximate broad regulatory sequence statistics and motif
grammar.

The library will therefore be synthetic but biology-informed:

- Use a broad motif panel covering ubiquitous and lineage-diverse transcription
  factor families rather than exact cell-line-specific ChIP peaks.
- Generate naturalistic backgrounds with varied GC, CpG, dinucleotide bias,
  low-complexity tracts, and weak motif-like subsequences.
- Include randomized controls and dinucleotide-preserving shuffles.
- Include controlled grammar sweeps over spacing, orientation, copy number,
  motif strength, and background composition.

## First design decision

I will make `generate.py` deterministic and dependency-free. It will write
exactly 50,000 unique 200 bp sequences with only A/C/G/T. I will divide the
library into strata so no single assumption dominates the design.

## Generator design

I wrote a self-contained generator with seven strata:

1. Backgrounds: 7,000 sequences with broad GC, CpG, dinucleotide persistence,
   and occasional low-complexity tracts. These are intended to teach baseline
   sequence effects and provide non-regulatory examples.
2. Single motif examples: 8,000 sequences containing one to three copies of a
   TF motif in varied backgrounds. This isolates individual motif effects.
3. Clusters: 11,000 enhancer-like motif clusters with three to seven motifs,
   sometimes with a second cluster. This represents dense cis-regulatory
   modules.
4. Pair sweeps: 8,000 controlled two-motif constructs varying TF pair,
   spacing, orientation, motif strength, GC, and CpG. This is the most direct
   grammar-learning component.
5. Promoters: 6,000 promoter-like sequences split between TATA/Inr-like
   architectures and CpG/SP1/KLF/NF-Y/E-box-rich architectures.
6. Mutational series: 5,000 related designs containing intact motif clusters,
   weakly mutated versions, stronger mutations, shuffles, and leave-one-motif
   variants. These should give a model local contrasts.
7. Negatives: 5,000 random, shuffled, muted, low-complexity, and extreme-GC
   backgrounds.

The motif panel is deliberately broad: AP-1, CREB, ETS, SP1/KLF, E-box,
NF-kB, GATA, FOX, RUNX, TEAD, SMAD, nuclear receptor half-sites, SOX/POU,
p53-like half-sites, TATA/Inr, NF-Y, IRF, STAT, RFX, ZEB, and CTCF-like
motifs. This is not a cell-line-specific panel; it tries to cover common
families and regulatory mechanisms.

I chose exact uniqueness over intentional replication. Replication would help
estimate measurement noise in a real MPRA, but the scoring appears to value
training information from a fixed-size library, so unique contrasts are likely
more valuable than replicate molecules.

## Execution note

The environment does not have a `python` executable (`python: command not
found`), so I will use `python3` for local generation and the final
`prepare.py` run.

## Validation before black-box evaluation

I generated `library/sequences.txt` with `python3 library/generate.py`. The
generator reported 50,000 sequences, GC min/mean/max of 0.115/0.512/0.895, and
a broad rounded GC distribution centered near 0.5. Independent checks showed:

- `wc -l library/sequences.txt`: 50,000
- invalid length or alphabet lines: 0
- unique lines after sorting: 50,000

I also added a root `generate.py` entry point so the requested project-level
script exists; it delegates to the implementation in `library/generate.py`.

## Black-box evaluation result

I ran the required one-shot evaluation with
`python3 prepare.py library/sequences.txt`. It completed in 888.9 seconds and
wrote `library/result.json`.

The mean_r values were:

- eval_01: 0.6617
- eval_02: 0.7458
- eval_03: 0.7211
- eval_04: 0.7048
- eval_05: 0.6615
- eval_06: 0.7462
- eval_07: 0.6428
- eval_08: 0.6821
- eval_09: 0.7636
- eval_10: 0.6991
- eval_11: 0.6502
- eval_12: 0.6214
- eval_13: 0.6461
- eval_14: 0.7461

The unweighted average over the 14 mean_r values is 0.6923214286, so the
commit message should use `oneshot: mean_r=0.692`.

## What I would try next

If I had another shot, I would compare this synthetic design against a hybrid
library that includes real genomic 200 bp windows from diverse ENCODE/FANTOM
enhancers, promoters, conserved noncoding elements, negative genomic regions,
and dinucleotide-preserving shuffles. The lowest results here were eval_12,
eval_07, eval_13, eval_11, and eval_01/eval_05, which suggests the synthetic
grammar was useful but may be missing natural genomic covariates or specific
sequence classes present in some test sets. I would also tune the fraction of
pair sweeps versus naturalistic genomic backgrounds, because the repeated high
scores on eval_02, eval_06, eval_09, and eval_14 imply that motif grammar
coverage helped some targets substantially.
