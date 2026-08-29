# 001 — Random baseline

## What I tested
50,000 iid uniform 200bp DNA sequences (seed=42). Pure noise floor.

## Result
- eval_01 mean_r = 0.116 (primary)
- Mean of evals: ~0.11 (range 0.05 – 0.12)
- K562: essentially 0 (-0.005 to 0.012)
- HepG2: 0.14–0.16
- SK-N-SH: 0.17–0.19 (best)
- eval_08 is an outlier: 0.053 mean_r
- Several evals report bit-identical numbers (01==14, 02==05, 04==09,
  03==12, 06==11), suggesting eval pairs use the same target sequences
  or differ only in something downstream — there are really ~7 distinct
  evals.

## What this means
- Random library teaches K562 model nothing — K562 activity must depend
  on motif presence absent from random sequences.
- SK-N-SH activity has some signal predictable from base composition or
  chance motif-like patterns in random DNA.
- The 0.11 number is the floor: any library that doesn't beat this is
  worse than noise.

## Theory update
- Confirms that pure random is a weak training set, but not zero.
- The fact that SK-N-SH does ~0.18 on a random library suggests some
  cell types have activity profiles partly predictable from low-order
  sequence statistics (GC content, dinucleotide frequencies).
- K562 needs motif structure to be learnable.

## What to try next
Experiment 002: embed diverse TF motifs in random backgrounds.
Hypothesis: providing motif signal will dramatically improve K562
(currently at noise) and also push HepG2/SKNSH up.
