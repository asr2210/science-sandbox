# 003 — Simple repeat motifs inserted into uniform random

## Setup
50K uniform-random length-200 backgrounds, one 12-bp simple motif inserted at
random position per sequence. 4 motifs (M1=010101..., M2=001100..., M3=121212...,
M4=012301...), 12,500 sequences per motif.

## Results
- eval_01 = 0.0393 (baseline 0.0420; Δ ≈ −0.003, within noise)
- eval_08 = 0.1116 (baseline 0.1242; Δ ≈ −0.013)
- All values close to baseline; no significant boost

## Inference
- Simple low-complexity repeat motifs occupying 6% of sequence don't move the
  score
- Either: (a) these patterns are not "motifs" the model recognizes, or (b)
  motif content at this density doesn't matter, or (c) motifs need to be of
  realistic biological character (not pure repeats)

## Next direction
Try biological-style motifs (TF consensus sequences encoded in {0,1,2,3}) with
higher per-seq coverage. If those help, real motif content matters.
