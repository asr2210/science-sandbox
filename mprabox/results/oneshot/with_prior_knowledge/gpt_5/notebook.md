# MPRA Library Design Notebook

## Initial reading

The task is to design exactly 50,000 200 bp DNA sequences for a one-shot MPRA
training library. The objective is not cell-line specialization for K562, HepG2,
or SK-N-SH, but general regulatory grammar across cell types. I will treat the
evaluation as a black-box assay and call `prepare.py` only once at final
submission.

The provided baseline table is highly informative. At 50k, DHS-based libraries
are the best-performing family, especially topic-weighted DHS sampling. Random
synthetic DNA helps some evaluations but hurts others; SEI mixtures diversify
annotations but do not clearly improve the 50k setting. My working hypothesis is
that the best 50k library should be mostly real accessible regulatory DNA, sampled
to cover many activity programs, with a smaller amount of deliberately perturbed
or background sequence to teach negative and intermediate grammar.

## Theory

A strong regulatory-sequence training set should expose the model to:

1. Real cis-regulatory grammar: TF motifs, motif spacing, GC/CpG structure,
   promoter/enhancer architecture, and local dinucleotide context.
2. Diverse tissue programs: the library should not collapse onto one or a few
   cell types.
3. Nonfunctional or weakly functional backgrounds: a model trained only on active
   elements may calibrate poorly and overpredict motif-like sequence.
4. Boundary cases: shuffled, mutated, and flanking genomic sequences should help
   distinguish motif content from broader genomic composition.

Given the baseline results, I will make DHS-centered sampling the default and
only add diversity if it is plausibly useful at 50k. The core design goal is high
information density rather than exhaustive coverage.

## Data plan

Allowed public data sources include the Meuleman DHS index and hg38 reference
sequence. I will download public reference files into `data/`, then generate
sequences in `library/`. I will not read prior run artifacts or any files outside
this run except public reference data.

## Implementation plan

I downloaded the public hg38 DHS index, the 16-component NMF mixture array, and
the UCSC hg38 2bit reference. The DHS table has 3,591,898 rows and the NMF
mixture has shape 16 x 3,591,898, so each mixture column corresponds to one DHS
row. I will use the summed NMF loadings as the main sampling weight, with a square
root transform to keep high-loading sites favored without letting the strongest
ubiquitous sites take too much of the 50k budget.

The current library recipe is:

1. 42,000 summit-centered 200 bp windows from topic-weighted DHS rows.
2. 3,000 dinucleotide-pair shuffles of DHS sequences as hard compositional
   negatives.
3. Several thousand flanking genomic windows offset from selected DHS summits.
4. GC-stratified synthetic random sequence to fill the remainder exactly to
   50,000.

This is intentionally closer to the best DHS-topic baseline than to the lower
performing half-random baselines. The added controls are a small tail meant to
improve calibration on weak/background sequence while preserving most library
capacity for real regulatory sequence.

## Pre-evaluation validation

I implemented `generate.py` with a small pure-Python 2bit reader because the
local environment did not have a usable 2bit Python package and I wanted to
avoid expanding hg38 to multi-gigabyte FASTA. I verified the reader against the
known chrM prefix (`GATCACAGGTCTATCACCCT`), which confirms the 2bit base encoding
is correct.

The generated `library/sequences.txt` has:

- 50,000 lines
- 50,000 unique sequences
- every sequence exactly 200 bp
- only A/C/G/T characters
- overall GC fraction 0.467

This is the final submitted library design before the one allowed evaluation
call.

## If I had another shot

The main unresolved question is the optimal size of the non-DHS control tail.
The baseline table shows random sequence improves at least one evaluation but
hurts the DHS-topic mean on many others. With iteration I would sweep mixtures
around 90-98% DHS topic-weighted sequence and compare pure random, flanking
genomic, dinucleotide-shuffled DHS, and cCRE promoter/enhancer controls. In this
one-shot setting I kept the control fraction modest and prioritized the known
strong DHS-topic backbone.

## Final evaluation

I ran the one allowed evaluation with:

```bash
python prepare.py library/sequences.txt
```

The run completed in 552.7 seconds and wrote `library/result.json`. The mean
across the 14 anonymous `mean_r` values is 0.7346. The individual eval mean
scores were:

| eval | mean_r |
| --- | ---: |
| eval_01 | 0.6977 |
| eval_02 | 0.7887 |
| eval_03 | 0.7695 |
| eval_04 | 0.7497 |
| eval_05 | 0.6978 |
| eval_06 | 0.7886 |
| eval_07 | 0.7184 |
| eval_08 | 0.6496 |
| eval_09 | 0.8100 |
| eval_10 | 0.7584 |
| eval_11 | 0.6857 |
| eval_12 | 0.6616 |
| eval_13 | 0.7201 |
| eval_14 | 0.7885 |

The result is weaker than I hoped relative to the provided DHS-topic baseline.
My likely mistake was allocating too much of the 50k budget to controls and
filtering the DHS draw toward high-signal rows after sampling. In another run I
would stay closer to pure topic-weighted DHS, then add a much smaller 1-5%
control tail only if there were validation evidence that it improves the broad
average.
