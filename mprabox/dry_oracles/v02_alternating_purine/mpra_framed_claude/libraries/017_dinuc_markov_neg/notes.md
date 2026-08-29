# Experiment 017 — dinucleotide-Markov negatives (worse than flanks)

## Design
- 25K positives (15K uniform + 5K CTCF + 5K DNH3, same as 013)
- 25K dinucleotide-Markov negatives generated from positives' global
  dinucleotide transition matrix.

## Result — mean_r 0.141 (worse than 013's 0.166)
| eval | 013 | 017 |
|------|-----|-----|
| 06/11 |**0.218**|0.181|
| 07    |**0.177**|0.145|
| 10    |**0.151**|0.103|
| 13    |0.126    |0.129|
| mean  |**0.166**|0.141|

## Interpretation
Composition-matched but motif-free negatives are NOT as informative
as paired flanks. The model loses the geographic context signal that
flanks provide.

eval_06/11 still decent (0.181, retains most enhancer signal). But
eval_07 and eval_10 drop substantially — those evals need the
geographic/positional info that flanks give.

## Theory T16
- Paired flanks > composition-matched negatives. Geography matters.
- The model is learning more than just motif vs no-motif; it's
  learning motif-in-context vs context-without-motif.

## Next
018 = multi-distance flanks. 60% far (1500-3000bp) + 40% near
(500-1500bp). Tests if multi-scale negatives capture both eval_06/11
(far-flank-friendly) and eval_10/13 (near-flank-friendly) signals.
