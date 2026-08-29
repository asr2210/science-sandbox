# 002_all_zeros

## Setup
50,000 identical copies of "0"*200.

## Results
All evals: NaN. Warning emitted:
  `eval/harness.py:111: ConstantInputWarning: An input array is constant;
  the correlation coefficient is not defined.`

## Key insight
**The score is a Pearson correlation coefficient (r)** — that's what "mean_r"
means. Constant input → undefined r → NaN.

Either per-string r (averaged), or column-wise r over the library matrix.
Need to test next.

## Parent directory hint
"MPRAgent_adversarial" — this looks like an MPRA (Massively Parallel Reporter
Assay) task. Alphabet {0,1,2,3} likely = nucleotides {A,C,G,T} (mapping unknown).
The scoring function probably mimics a trained model predicting regulatory
activity from 200bp DNA sequences. 14 evals could be different cell types or
assay conditions; condition_a/b/c subgroups within each.

## Implications
- We need intra-string and likely cross-string variation
- We need to find sequences that correlate with whatever target the eval model
  uses (probably some "activity" prediction)
- Random scores ~0.5, so 0.5 isn't terrible — we want >> 0.5
