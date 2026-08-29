# MPRA Library Design Notebook

## Initial interpretation

The task is to design a fixed 50,000-sequence, 200 bp MPRA training library for
learning regulatory grammar that generalizes beyond K562, HepG2, and SK-N-SH.
I am treating the evaluator as a black-box assay: I will not inspect
`prepare.py`, and I will make the library before running it once.

The central design problem is active learning without feedback. A good library
should expose a model to broad regulatory sequence variation: real genomic
context, motif syntax, motif combinations, negative/background sequence, GC and
CpG regimes, repeat-like structure, and systematic perturbations. Because the
goal is general grammar rather than maximizing activity in three assayed cell
lines, I should avoid overfitting to K562/HepG2/SK-N-SH-specific enhancers and
instead cover sequence features used by many transcriptional systems.

## Working theory

Regulatory activity depends on several layers:

- Local motif content: TF binding sites, orientation, affinity, degeneracy,
  spacing, and copy number.
- Motif grammar: cooperative or antagonistic combinations, homotypic clusters,
  heterotypic clusters, promoter-like initiator/TATA/GC-box patterns, and
  enhancer-like dispersed syntax.
- Sequence background: GC content, CpG density, poly-A/T or low-complexity
  tracts, nucleosome-disfavoring periodicity, and genomic-like dinucleotide
  structure.
- Context and controls: flanks and null sequences matter because models must
  learn what is not regulatory as well as what is regulatory.

Therefore I plan to mix several sequence classes rather than produce only
known active elements. The library should include designed motif examples with
controlled syntax, random/background examples across compositional regimes, and
perturbation series that teach the model causal motif effects.

## Sources and constraints considered

The instructions allow web/data downloads, but the run has no iteration after
evaluation. For reliability I will use a self-contained motif set rather than
depending on a large external genome download. This reduces the chance of
format or network problems and lets the generator exactly reproduce the final
library. I will encode a broad panel of canonical metazoan regulatory motifs
as IUPAC consensus patterns, then sample variants from them. This is less rich
than using the full human genome and motif databases, but it directly creates
diverse, interpretable regulatory grammars and avoids making the library too
tissue-specific.

## Planned library composition

I will generate exactly 50,000 200 bp sequences from deterministic components:

1. Background controls spanning GC bins and dinucleotide-like local structure.
2. Single-motif and affinity-ladder examples for broad TF families.
3. Homotypic motif clusters with varied copy number, spacing, orientation, and
   background GC.
4. Heterotypic enhancer-like clusters sampling many TF-family combinations.
5. Promoter-like sequences containing TATA/Inr/GC-box/CCAAT motifs plus
   variable distal motifs.
6. Systematic perturbation pairs/series: motif-present vs motif-mutated,
   spacing sweeps, copy-number sweeps, and orientation flips.
7. Decoy and hard-negative sequences preserving composition while scrambling
   motif instances.

This mixture should improve training performance per sequence because each
design contributes controlled information, while the randomization prevents a
model from only memorizing a narrow motif grammar.

## Generator implementation

I implemented `generate.py` as a deterministic script using seed 732451. The
motif source is an embedded set of broad IUPAC consensus motifs covering signal
response factors, promoter factors, pioneer factors, hematopoietic factors,
neural/developmental factors, nuclear receptors, architectural factors, stress
response factors, and metabolic/structural factors.

The exact category allocation is:

- 7,000 background controls across iid, Markov-like, CpG-enriched/depleted,
  and low-complexity regimes.
- 7,000 single-motif examples, including some weakened affinity variants.
- 9,000 homotypic clusters with variable copy number, spacing, orientation,
  and sequence background.
- 14,000 heterotypic clusters sampling multiple TF-family combinations per
  sequence.
- 6,000 promoter-like sequences with probabilistic TATA, Inr, CCAAT, GC-box,
  KLF, and distal regulatory motifs.
- 5,000 perturbation-style sequences produced in small batches: motif-present,
  motif-mutated, motif-weakened, and orientation-flipped variants.
- 2,000 decoys made by locally shuffling motif-rich sequences to preserve
  approximate composition while disrupting exact motif grammar.

I chose this balance because heterotypic syntax is likely the highest-value
class for learning general regulatory grammar, while backgrounds and decoys are
needed to prevent the model from treating all nonrandom sequence as active.
Promoter-like sequences are included, but not dominant, because enhancer and
promoter grammar overlap only partially and the hidden evaluations may contain
both.

## Pre-evaluation validation

After generating the library with `python3 generate.py`, I checked:

- Line count: exactly 50,000.
- Length/alphabet: zero sequences failed the 200 bp and A/C/G/T-only checks.
- Duplicates: zero duplicate sequences.
- GC distribution: minimum 0.065, mean approximately 0.505, maximum 0.920;
  7,519 sequences are GC < 0.35, 34,826 are between 0.35 and 0.65, and 7,655
  are GC > 0.65.

The extreme GC tails are intentional. They may be less genomic on average, but
they give the model informative negatives and positives for compositional
effects, CpG-rich promoter-like contexts, and AT-rich low-complexity contexts.
Most sequences remain in the broad genomic middle.

## One-shot evaluation result

I ran the black-box evaluation with `python3 prepare.py library/sequences.txt`
because this environment does not provide a `python` executable. The run
completed in 599.3 seconds and wrote `library/result.json`.

Per-set mean correlations:

- eval_01: 0.5570
- eval_02: 0.6286
- eval_03: 0.5941
- eval_04: 0.6109
- eval_05: 0.5565
- eval_06: 0.6304
- eval_07: 0.5203
- eval_08: 0.5609
- eval_09: 0.6596
- eval_10: 0.5784
- eval_11: 0.5482
- eval_12: 0.5112
- eval_13: 0.5109
- eval_14: 0.6291

The aggregate mean of the 14 `mean_r` values is 0.578293, so I will use
`oneshot: mean_r=0.578` as the commit message.

## What I would try next

With another shot, I would add a controlled fraction of real genomic regulatory
and matched non-regulatory sequence windows, ideally sampled across cCRE
classes, promoters, intronic/intergenic background, and repeat-masked contexts.
The current library is intentionally self-contained and grammar-heavy; adding
real genomic context could improve performance on hidden test sets that are
closer to naturally occurring regulatory elements. I would also run small
ablation studies over the category mix if iteration were allowed, especially
varying the heterotypic/promoter/background ratios and the number of extreme-GC
background controls.
