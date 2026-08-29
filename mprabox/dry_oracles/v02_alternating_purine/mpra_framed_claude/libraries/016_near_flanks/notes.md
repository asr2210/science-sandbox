# Experiment 016 — near flanks (500-1500bp) hurt the model

## Design
- Same positives as 013 (15K uniform + 5K CTCF + 5K DNH3)
- 25K NEAR flanks: 500-1500bp offset (vs 013's 1500-3000bp)

## Result — mean_r 0.135 (much worse than 013's 0.166)
| eval | 013 | 016 |
|------|-----|-----|
| 06/11 |**0.218**|0.135|
| 07    |**0.177**|0.157|
| 10    |0.151    |**0.161**|
| 13    |0.126    |**0.151**|
| mean  |**0.166**|0.135|

K562_r goes NEGATIVE on most evals. eval_06/11 collapses.

## Interpretation
500-1500bp flanks are TOO close — too similar in chromatin context.
The model cannot find robust discriminative features and ends up
confusing positives with their near-neighbor windows. K562 enhancer
signal is destroyed.

Bright spots: eval_10/13 improve (+0.01, +0.025). Closer flanks help
those evals specifically — possibly because they tolerate noisier
discrimination.

## Theory update (T15 → T16)
- 1500-3000bp flank distance in 013 is well-tuned.
- Near flanks (<1500bp) are too hard; far flanks (>3000bp) would
  likely be too easy.
- The eval_10/13 lift from near flanks is interesting — might mean
  those evals reward specific motif content rather than chromatin-
  context discrimination.

## Next
017 = different negative TYPE: dinucleotide-Markov-sampled
sequences. Use the global dinucleotide statistics of the positives
to sample fresh negatives. Composition-matched but structure-free.
Forces the model to learn motifs beyond dinucleotide patterns.
