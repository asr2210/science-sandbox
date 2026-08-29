# 009 Markov dinucleotide bias

1st-order Markov: AT-favored, CpG (12->21) suppressed.

## Result
- eval_01 = 0.1788 (vs 0.2974). BIG drop.
- My bias choice was wrong; the eval distribution dislikes my Markov.
- eval_07 and 13 are relatively preserved.
