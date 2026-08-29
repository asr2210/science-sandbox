# 010_repeatmasked_genomewide — notes

## Design
50K x 200bp uniform-random windows from hg38 main chromosomes
(same as exp 009), but reject any window that is >50% soft-masked
(repeat content from RepeatMasker + Tandem Repeats Finder embedded
in hg38.2bit). N-rejected ~5%, repeat-rejected ~50%, kept ~45%.
Sequences are uppercased before writing.

## Hypothesis
Tests whether repeats are the active distractor that made exp 009
underperform uniform random ACGT. If repeat-masking recovers most
of the gap (genwide 0.690 → cCRE 0.748), repeats are the entire
problem. Otherwise, the cCRE annotation captures more than just
"non-repeat".

## Result vs. previous

| eval | rand   | cCRE   | dELS   | genwide | **rmask** | Δ(rmask−genwide) | Δ(rmask−rand) |
|------|--------|--------|--------|---------|-----------|-------------------|----------------|
| 01   | 0.6954 | 0.7133 | 0.7090 | 0.6596  | 0.6538    | -0.006            | -0.042         |
| 02   | 0.7848 | 0.8046 | 0.8014 | 0.7424  | 0.7364    | -0.006            | -0.048         |
| 03   | 0.7612 | 0.7870 | 0.7897 | 0.7332  | 0.7217    | -0.012            | -0.040         |
| 04   | 0.7494 | 0.7733 | 0.7417 | 0.6922  | 0.6799    | -0.012            | -0.069         |
| 05   | 0.6951 | 0.7133 | 0.7089 | 0.6605  | 0.6541    | -0.006            | -0.041         |
| 06   | 0.7853 | 0.8048 | 0.8017 | 0.7433  | 0.7373    | -0.006            | -0.048         |
| 07   | 0.6684 | 0.7452 | 0.7605 | 0.7120  | 0.6905    | **-0.022**        | +0.022         |
| 08   | 0.7841 | 0.6380 | 0.6720 | 0.5351  | 0.5891    | **+0.054**        | -0.195         |
| 09   | 0.8115 | 0.8385 | 0.8042 | 0.7463  | 0.7341    | -0.012            | -0.077         |
| 10   | 0.7564 | 0.7635 | 0.7779 | 0.6808  | 0.6896    | +0.009            | -0.067         |
| 11   | 0.6833 | 0.7010 | 0.6973 | 0.6497  | 0.6436    | -0.006            | -0.040         |
| 12   | 0.6553 | 0.6757 | 0.6782 | 0.6320  | 0.6226    | -0.009            | -0.033         |
| 13   | 0.6584 | 0.7422 | 0.7601 | 0.7326  | 0.7108    | **-0.022**        | +0.052         |
| 14   | 0.7851 | 0.8046 | 0.8015 | 0.7413  | 0.7360    | -0.005            | -0.049         |

Mean across evals: rand 0.738, cCRE 0.748, dELS 0.756, genwide
0.690, **rmask 0.686**.

## Interpretation

**Repeat-masking did not recover any of the genome-wide gap to
cCRE — and slightly worsened the mean (0.690 → 0.686).** The
hypothesis "repeats are the active distractor" is **falsified**.

The per-eval pattern is sharp:
- **eval_08 +0.054**: removing repeats helps the
  uniform-comp-loving eval. Confirms repeats are bio-flavored
  enough to hurt eval_08, but they aren't the whole story
  (eval_08 still 0.589 vs random's 0.784).
- **eval_07 −0.022, eval_13 −0.022**: the two motif-rewarding
  evals get WORSE without repeats. Repeats actually carry useful
  TF motif content (LTR retroviruses harbor real TFBSes that
  affect regulation; SINEs contain real binding sites).
- Most other evals: ~−0.005 to −0.012, basically noise.

Net: repeats are not a uniform distractor. They contain real
biological signal (TF motifs from transposon-derived sequences)
that helps motif-rewarding evals, while contributing noise on
the synthetic-favoring eval_08.

## What this changes (theory update)

Major refinement:
> The genome-wide failure (exp 009) is NOT caused by repeats.
> Even repeat-masked genomic random is worse than uniform random
> ACGT. The dominant cause must be the non-repeat
> intergenic/intronic content: vast tracts of low-complexity but
> non-repetitive sequence (gene deserts, AT-rich isochores,
> introns) that lack regulatory grammar but introduce real
> sequence patterns the model learns and over-applies.

Updated framing:
> Curation matters because the bulk of the human genome is
> low-information for regulatory tasks — neither random enough
> to teach generic features nor regulatory enough to teach
> specific grammar. cCRE annotation specifically picks the ~0.7%
> of the genome that lies in the high-information regulatory
> tail. "Repeat content" is a distinct (and partially helpful)
> signal that sits inside the same low-information bulk.

## Per-eval signal partition: repeats add motifs, remove
composition

This experiment cleanly decomposes the genome-wide content:
- Repeat content → +motif signal (helps 07, 13) but
  +bio-content distraction (hurts 08).
- Non-repeat non-regulatory → uniformly low-info on every eval.

The cCRE library captures motif content WITHOUT the diluting
non-regulatory bulk. That's the real win.

## Next experiment

The next sharp question: **is dELS-specifically-good, or is "any
single large cCRE class" good?** dELS has 1.47M elements; CA has
~250K; CA-CTCF ~125K; pELS ~250K. CA is the second-largest broad
class.

**Exp 011: CA-only library.** 50K x 200bp from the ~250K CA pool.
- If CA-only ≈ dELS-only → "any large within-class pool works",
  the dELS win was about pool size.
- If CA-only ≪ dELS-only → dELS has something specific (likely
  cell-type-specific enhancer grammar that CA elements lack).
- If CA-only ≫ dELS-only → CA is even better (chromatin
  accessibility content is more informative than enhancer
  content).

This isolates the "pool size" hypothesis from the
"dELS-specifically" hypothesis.
