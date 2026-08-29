# 023 — Variable density (N_MOTIFS in {0..5} uniform)

## Setup
17 TFs / random N_MOTIFS per seq from {0,1,2,3,4,5} (uniform mix).

## Results
eval_01 = 0.3371. Worse than fixed 3/seq (0.3644).

## Insight
A wider density distribution does NOT help Spearman, despite intuition that
bimodal predicted-activity should improve ranking. The eval likely uses
mostly within-band ranking, so uniform optimal density (3/seq) dominates.
