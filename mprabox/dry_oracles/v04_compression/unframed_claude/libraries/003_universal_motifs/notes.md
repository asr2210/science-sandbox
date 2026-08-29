# 003 — Random + universal TFBSs (~6/seq)

## Hypothesis
Embedding strong universal regulatory motifs (TATA, SP1, AP-1, CCAAT, ETS,
CREB, E-box, KLF, NRF1, YY1) at random positions on a uniform-random scaffold
should beat the random baseline.

## Setup
50k x 200bp. Each sequence: uniform random base, 4–8 motifs from a 14-element
set sampled and placed at non-overlapping random positions.

## Results
eval_01 = **0.3205** (random was 0.3157; +0.005 — noise).
eval_07 = 0.4543 (vs 0.4481; +0.006).
eval_08 = 0.0630 (vs 0.1032; **−0.040**).
eval_10 = 0.3297 (vs 0.3792; **−0.050**).
eval_13 = 0.4095 (vs 0.4201; −0.011).
Net: about flat, with notable drops on some evals.

## Key observations
- 6 motifs per sequence is a real perturbation (~21% of 200bp), yet eval_01
  barely changes. Either these motifs aren't what the scorer cares about, or
  motif insertion as a strategy is wrong.
- Drops on eval_08 and eval_10 suggest some evals dislike the inserted motifs,
  possibly because they're disrupting natural k-mer statistics.
- eval_04 and eval_09 are now exactly equal (0.2681). They were also equal in
  001 and 002. Confirms 04==09 are a duplicate eval.

## Update to theory v3
Inserting short universal motifs is not the right lever. The scorer is
probably looking at richer / longer features: position-weight matrices,
multi-motif co-occurrence, or genome-like k-mer statistics. Uniform random
already contains all the accidental short motifs; adding ~6 more doesn't
move the needle.

Two competing hypotheses:
(a) Need REAL biological sequences (downloaded human enhancers).
(b) Need very HIGH-density motif stacking (pack the sequence with motifs).

## Next
Experiment 004: pack each sequence with high-density motif stacks (15–25
motifs / seq, possibly tandem). If still flat → hypothesis (a). If improves
→ density is the lever.
