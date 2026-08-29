# 010 shotgun_mixed

10 generation methods × 5000 each = 50,000. Methods: random uniform, Dirichlet(0.1),
Dirichlet(1.0), Markov DNA-like, 4-mer repeats, 8-mer repeats, motif "01230123",
motif "00033330", AT-rich, GC-rich.

## Result
eval_01 = +0.0005 (worse than Dirichlet alone +0.0030).
**eval_13 = +0.0079** (best mean_r on any eval to date), condition_c = +0.0188.
eval_03/12 = +0.0034.

## Interpretation
- eval_01 mean diluted by mixing — dirichlet alone wins.
- eval_13 LOVES diversity — shotgun perfect for it.
- Different evals reward fundamentally different libraries.

## Key takeaway for eval_01
Adding low-complexity / motif / GC-bias sequences HURTS eval_01.
Dirichlet (composition diversity, but each sequence still high-entropy) wins.

## Next
Push composition diversity further. Try diverse per-sequence Markov chains
(diversifies dinucleotide stats, not just compositions).
