# MPRA Library Design Notebook

## Initial objective interpretation

The task is to design a 50,000 sequence, 200 bp MPRA training library for a model
that generalizes across regulatory grammar rather than across only K562, HepG2,
and SK-N-SH. I interpret this as an experimental design problem: the useful
training set should span sequence features that plausibly control regulatory
activity, while also including negatives and decoys so the model learns
specificity.

I will treat the evaluator as a black-box assay. I will not use it for iterative
optimization; the library must be designed once, then evaluated once.

## Theory of a good library

A compact MPRA training set should have high information per assayed sequence.
For cis-regulatory modeling, that means sampling across:

- Background composition: GC fraction, CpG content, homopolymer tendency,
  dinucleotide structure, and low-complexity avoidance.
- Motif identity: broadly used transcription factor motifs such as SP/KLF,
  ETS, AP-1/CREB, E-box factors, GATA, FOX, nuclear receptors, interferon and
  immune motifs, CTCF-like motifs, promoter elements, and developmental TFs.
- Motif dose: zero, one, two, and many motif copies.
- Motif grammar: orientation, spacing, clustering, homotypic and heterotypic
  combinations, promoter-like arrangements, enhancer-like clusters, and
  insulation-like motifs.
- Counterexamples: scrambled motifs, near-miss motifs, reverse complements,
  GC-matched random sequences, and sequences that contain partial motifs only.

The library should not be only active enhancers. A model trained only on
functional-looking sequences can overfit to obvious high-activity motif
clusters and fail on weak, silent, or composition-driven examples. I therefore
plan to allocate a large fraction to controlled synthetic sequences with known
motif manipulations and a meaningful fraction to realistic-but-random
backgrounds.

## Data/source decisions

I considered downloading genome windows, ENCODE cCREs, and JASPAR motif PWMs.
Because this is a one-shot run and the evaluator is anonymous, I prefer a
self-contained deterministic generator using a hand-curated set of common IUPAC
motif patterns. This avoids dependence on a particular genome build or tissue
annotation and keeps the resulting design explicitly general rather than tied to
available K562/HepG2/SK-N-SH functional catalogs.

I will still create a `data/` directory per the instructions, but at this point
there is no need to download external data. The library will be generated from
general regulatory design principles.

## Planned library strata

The generator will produce a fixed, shuffled 50,000 sequence set:

- GC/dinucleotide background controls.
- Single motif insertions across many motif families, positions, orientations,
  copy counts, and GC backgrounds.
- Pair and triple motif grammar examples with varied spacing.
- Homotypic motif clusters to teach dose response.
- Promoter-like constructs with TATA, INR, BRE/DPE-like, CCAAT, GC-box, and
  initiator elements.
- Enhancer-like constructs mixing ubiquitous, signaling, lineage, and
  developmental motifs without targeting one tissue.
- Mutational contrast examples: motif-bearing sequences paired with motif
  scramble or one/two-base disrupted versions.
- Hard negatives: GC-matched random, partial motifs, low-complexity safe
  backgrounds, and shuffled high-motif-count sequences.

## Implementation notes

I will write `generate.py` so the exact library is reproducible from a fixed
seed. It should validate count, length, alphabet, and uniqueness. Some duplicate
risk exists because random backgrounds are large, but deterministic duplicate
checking and regeneration will keep the final file valid.

## Generator implemented

I implemented `generate.py` as a deterministic synthetic design generator with a
fixed seed. It uses a hand-curated set of common IUPAC motif patterns covering
ubiquitous factors, promoter elements, signaling-responsive motifs, immune
motifs, bHLH, GATA/RUNX/TAL-like motifs, FOX, nuclear receptors, developmental
TFs, homeobox factors, architectural motifs, and stress-response motifs.

The final stratum allocation is:

- 8,000 background controls with IID, Markov-like, shuffled, GC-low, GC-mid,
  and GC-high sequences.
- 9,000 single-motif examples across positions, orientations, and backgrounds.
- 11,000 pairwise motif grammar examples with selected biologically plausible
  class pairings and spacings from adjacent to 64 bp.
- 8,000 triple-motif examples sampling common cross-class combinations.
- 5,000 homotypic clusters with two to six copies.
- 3,500 promoter-like sequences combining core promoter elements and upstream
  TF motifs.
- 3,500 enhancer-like dense motif clusters.
- 2,000 mutational contrast sequences, including inserted motifs and
  disrupted/scrambled motif decoys.

I chose this allocation to balance three goals: enough unmodified background to
learn composition and silence, enough simple motif examples to identify
individual sequence features, and enough combinatorial examples to teach
spacing, orientation, dose, and heterotypic grammar.

## Validation before evaluation

I ran the generator and checked the resulting `library/sequences.txt`.

- Number of lines: 50,000.
- Unique sequences: 50,000.
- Invalid length or alphabet: 0.
- All sequences are exactly 200 bp.
- Mean GC fraction: 0.5067.
- GC range: 0.165 to 0.835.
- GC quantiles: 5% = 0.310, 10% = 0.345, 25% = 0.415, 50% = 0.510,
  75% = 0.600, 90% = 0.665, 95% = 0.695.

The GC distribution is broad enough to cover AT-rich promoter-like or
developmental contexts, CpG/GC-rich promoter-like contexts, and balanced
enhancer-like backgrounds. The extremes are present but not dominant, which
should avoid wasting too many assays on composition outliers.

## Final pre-assay decision

I will proceed with this library for the one allowed evaluation. I am not
iteratively optimizing against the evaluator. The design is intentionally broad,
synthetic, and interpretable, with realistic regulatory primitives but no
dependency on one cell type's active element catalog.

## Evaluation result

I ran `python prepare.py library/sequences.txt` once. The evaluator completed in
603.6 seconds and wrote `library/result.json`.

Per-evaluation results:

| eval | mean_r | K562 | HepG2 | SK-N-SH |
| --- | ---: | ---: | ---: | ---: |
| eval_01 | 0.6232 | 0.6067 | 0.6249 | 0.6379 |
| eval_02 | 0.7057 | 0.6863 | 0.7048 | 0.7260 |
| eval_03 | 0.6718 | 0.6518 | 0.6707 | 0.6930 |
| eval_04 | 0.6845 | 0.6805 | 0.6822 | 0.6909 |
| eval_05 | 0.6226 | 0.6054 | 0.6249 | 0.6375 |
| eval_06 | 0.7061 | 0.6856 | 0.7056 | 0.7270 |
| eval_07 | 0.5849 | 0.5709 | 0.5844 | 0.5994 |
| eval_08 | 0.6553 | 0.6381 | 0.6592 | 0.6687 |
| eval_09 | 0.7398 | 0.7327 | 0.7388 | 0.7477 |
| eval_10 | 0.6521 | 0.6416 | 0.6502 | 0.6646 |
| eval_11 | 0.6121 | 0.5954 | 0.6155 | 0.6254 |
| eval_12 | 0.5768 | 0.5641 | 0.5762 | 0.5902 |
| eval_13 | 0.5665 | 0.5429 | 0.5653 | 0.5912 |
| eval_14 | 0.7064 | 0.6870 | 0.7056 | 0.7265 |

The average of the 14 `mean_r` values is 0.650557, which rounds to 0.651 for
the commit message.

## Retrospective and next ideas

The strongest anonymous sets were eval_09, eval_14, eval_06, and eval_02, all
around or above 0.706 mean_r. The weakest were eval_13, eval_12, and eval_07.
Without knowing the anonymous set definitions, my hypothesis is that the broad
motif grammar and GC/background variation worked reasonably well, but some test
sets may rely on more realistic genomic sequence context, longer-range motif
density distributions, or precise PWM variation that a hand-curated consensus
library does not fully cover.

If I had another shot, I would try a hybrid library: keep the same controlled
synthetic strata, but replace some singleton and dense-cluster capacity with
genome-sampled, repeat-masked, GC-stratified windows from many tissues and many
activity levels. I would also use real PWMs instead of consensus IUPAC motifs,
then design systematic affinity ladders for each motif family. That would better
teach weak-site behavior and motif degeneracy while preserving the current
controlled grammar coverage.
