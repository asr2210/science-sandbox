# 009 markov_per_seq

Per-sequence Markov chain with random transition matrix.

## Result
- eval_01: 0.3856 (vs 0.3917 at alpha=2.0)
- Slightly worse on primary metric
- eval_04/09: 0.4337 (improved)
- eval_08: 0.3333 (improved)

Adding per-sequence transition-matrix variance helps secondary evals but
doesn't beat unigram-composition variance on eval_01.

Next: try embedded k-mer motifs (per-sequence random motif) to add k-mer variance.
